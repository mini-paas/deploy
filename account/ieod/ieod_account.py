# -*- coding: utf-8 -*-
"""
账号体系相关的基类Account
"""
import time
import json
import random
import urllib
import urllib2
import urlparse

from suds.client import Client
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME

from account.accounts import Account
from account.utils import http_request_workbench


class IeodAccount(Account):
    """
    内部版
    """

    def __init__(self):
        self.env_code = 'ieod'
        super(IeodAccount, self).__init__()

    # ======================此部分提供公共方法， 验证用户登录态相关==============================
    def check_user_login_status(self, request, autoLogin=True):
        """
        @summary:  校验用户登录态
        @note: 登录态以cookie中的为准
        1）cookie中有效：
            a)session中无效，重新写session， 返回 0
            b)session中有效，返回0
        2）cookie中无效
            a)session中无效，返回-1
            b）sessoin中有效，清除session，返回-1
        0:登录态有效
        -1:登录态无效
        """
        if self._config.RUN_MODE == 'DEVELOP' or self._config.OA_LOGIN is True:
            # 从cookie拿bk_ticket
            oa_ticket = request.session.get('ticket', '')
            if oa_ticket == '':
                oa_ticket = request.GET.get("ticket", '')
            result, data = self.verify_oa_ticket(oa_ticket)
        else:
            # 从cookie拿bk_ticket
            bk_ticket = request.COOKIES.get('bk_ticket', '')
            # 校验ticket有效性
            result, data = self.verify_bk_ticket(bk_ticket, True)

        if result:
            is_bk_login = True
            # 判断 session中的登录态是否有效
            if request.user.is_authenticated():
                # 判断session 中用户信息和cookie中的用户信息是否一致
                if data.get('username', '') != request.user.username:
                    # 原有账号退出登录
                    auth.logout(request)
                else:
                    # 用户登录信息正确， 不需要再重新登录
                    is_bk_login = False
            if is_bk_login:
                user = auth.authenticate(request=request, user_info=data)
                self.bk_login(request, user, getattr(user, 'full_info', {}))
            # 登录态有效返回
            return 0
        # 清除 session 中的登录态
        if request.user.is_authenticated():
            # 后台登录态无效， 先清除 session登录态
            auth.logout(request)
        return -1

    def check_backend_login_status(self, request):
        """
        校验后台登录状态
        返回码：
        0 登录态有效
        -1 登录态无效
        """
        # 注意：内部版的登录有一点特别
        # 如果是开发环境， 则不使用统一登录， 只要员工进行了tof oa登录， cookie里面有ticket就可以了
        # 如果非开发环境， 则使用完整的统一登录
        if self._config.RUN_MODE == 'DEVELOP' or self._config.OA_LOGIN is True:
            # 从cookie拿bk_ticket
            oa_ticket = request.session.get('ticket', '')
            if oa_ticket == '':
                oa_ticket = request.GET.get("ticket", '')
            result, data = self.verify_oa_ticket(oa_ticket)
        else:
            # 从cookie拿bk_ticket
            bk_ticket = request.COOKIES.get('bk_ticket', '')
            # 校验ticket有效性
            result, data = self.verify_bk_ticket(bk_ticket, True)

        if not result:
            return False, {}

        # 检查此用户是否在django用户表里
        userName = data.get("username", "")
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=userName)
        except user_model.DoesNotExist:
            # 第一次登录的时候要新建一个user
            user = user_model(username=userName)
            user.save()

        setattr(user, 'full_info', data)
        return True, user

    def check_user_weixin_login_status(self, request):
        """
        0:登录有效
        -1:登录无效
        """
        # 从参数中拿 微信登录的用户票据code
        code = request.GET.get('code')
        state = request.GET.get('state')
        # 不存在code 或 state 则登录失败
        if not code or not state:
            return -1
        # 校验state是否正确
        if not self.verify_weixin_oauth_state(request, state):
            self._config.logger.error(u"微信登录校验state不正确:code[%s],state[%s]" % (code, state))
            return -1
        # 校验code有效性
        result, user_info = self.get_user_wx_info(code)
        if result:
            user = auth.authenticate(user_info=user_info)
            if not user:
                self._config.logger.error(u"微信登录出错:code[%s], user_info: %s" % (code, user_info))
                # 登录出错或无效 返回
                return -1
            self.bk_weixin_login(request, user, user_info)
            # 登录有效返回
            return 0
        # 登录出错或无效 返回
        return -1

    def get_user_wx_info(self, code):
        """
        @summary: 验证微信登录票据的有效性
        @param code: 用户票据
        @return: result, data
        @note: 调用统一登录的 weixin/get_user_info 接口，验证code的同时获取 username登录信息
        """
        result = False
        data = {}
        try:
            resp = urllib2.urlopen(self._config.WEIXIN_GET_INFO_URL % code).read()
            resp = json.loads(resp)
            ret = resp.get('ret', -1)
            # 验证成功，获取用户昵称
            if ret == 0:
                data = resp.get('data', {})
                result = True
            else:
                self._config.logger.info(u"通过code[%s]获取用户信息失败:%s" % (code, resp))
        except Exception, e:
            self._config.logger.error(u"通过code[%s]获取用户信息异常:%s" % (code, e))
        return result, data

    def set_weixin_oauth_state(self, request, length=32):
        """
        生成随机的state，并存储到session中
        """
        allowed_chars = 'abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'
        state = ''.join(random.choice(allowed_chars) for _ in range(length))
        request.session['WEIXIN_OAUTH_STATE'] = state
        request.session['WEIXIN_OAUTH_STATE_TIMESTAMP'] = time.time()
        return state

    def get_weixin_auth_code(self, request):
        """
        获取微信code
        """
        url = urlparse.urlparse(request.build_absolute_uri())
        path = '%s?%s=%s' % (self._config.WEIXIN_LOGIN_URL, REDIRECT_FIELD_NAME, url.path)
        url = urlparse.urlunsplit((url.scheme, url.netloc, path, url.query, url.fragment))
        state = self.set_weixin_oauth_state(request)
        redirect_uri = self.get_oauth_redirect_url(url, state=state)
        return HttpResponseRedirect(redirect_uri)

    def get_oauth_redirect_url(self, url, state='authenticated'):
        """
        获取oauth访问链接
        """
        params = {
            'appid': self._config.WEIXIN_APP_ID,
            'redirect_uri': url,
            'response_type': 'code',
            'scope': 'snsapi_base',
            'state': state
        }
        params = urllib.urlencode(params)
        redirect_uri = '%s?%s#wechat_redirect' % (self._config.WEIXIN_OAUTH_URL, params)
        return redirect_uri

    def verify_weixin_oauth_state(self, request, state, expires_in=60):
        """
        验证请求weixin code的 state参数是否一致
        """
        try:
            raw_state = request.session.get('WEIXIN_OAUTH_STATE')
            raw_timestamp = request.session.get('WEIXIN_OAUTH_STATE_TIMESTAMP')
            # 验证state
            if not raw_state or raw_state != state:
                return False
            # 验证时间戳
            if not raw_timestamp or time.time() - raw_timestamp > expires_in:
                return False
            # 验证成功后清空session
            request.session['WEIXIN_OAUTH_STATE'] = None
            request.session['WEIXIN_OAUTH_STATE_TIMESTAMP'] = None
            return True
        except Exception, e:
            self._config.logger.error(u"验证请求weixin code的 state参数出错： %s" % e)
            return False

    def verify_oa_ticket(self, oa_ticket):
        """
        通过ticket获取用户信息(OA验证), 2014-4-16 james edit
        """
        result = False
        data = {}
        try:
            soap_client = Client(self._config.PASSPORT_SERVICE_WSDL)
            staff = soap_client.service.DecryptTicket(oa_ticket)
            if not staff:
                self._config.logger.error(u"OA ticket无效，重新登录获取ticket")
                return result, data

            result = True
            data['username'] = staff.LoginName
            data['chinese_name'] = staff.ChineseName
            data['dept_id'] = staff.DeptId
            data['dept_name'] = staff.DeptName
            data['group_id'] = -1
            data['group_name'] = ''
            data['post_name'] = ''
            data['ticket'] = oa_ticket
        except Exception, e:
            self._config.logger.error(u"验证OA ticket失败， 异常信息 ： %s" % e)
        return result, data

    def verify_bk_ticket(self, bk_ticket, is_full=False):
        """
        @summary: 验证登录票据的有效性
        @param bk_ticket: 用户票据
        @param  is_full: 为Ture则查询用户的完整信息
        @return: result, data
        @note: 调用统一登录的 user/get_info 接口，验证cookie的同时获取 username，uin登录信息
        """
        result = False
        data = {}
        try:
            query_param = {'bk_ticket': bk_ticket}
            if is_full:
                req_url = self._config.GET_FULL_INFO
            else:
                req_url = self._config.GET_INFO_URL
            # 调用验证cookie接口的时长
            resp = http_request_workbench(req_url, 'GET', query_param)
            ret = resp.get('ret', -1)
            # 验证成功，获取用户昵称
            if ret == 0:
                data = resp.get('data', {})
                data['ticket'] = bk_ticket
                result = True
            else:
                self._config.logger.info(u"verify_cookie, bk_ticket:%s, ret:%s, data:%s, resp:%s" %
                                         (bk_ticket, ret, data, resp))
        except Exception, e:
            self._config.logger.error(u"验证用户（bk_ticket：%s）cookie的有效性出错:%s" % (bk_ticket, e))
        return result, data

    def bk_login(self, request, user, userInfo):
        """
        @summary: 登录
        """
        super(IeodAccount, self).bk_login(request, user)

        # 登录成功后，记录session
        if userInfo is None:
            return True
        request.session['ticket'] = userInfo.get("ticket", '')
        request.session['chinese_name'] = userInfo.get('chinese_name', '')
        request.session['dept_id'] = userInfo.get('dept_id', '-1')
        request.session['dept_name'] = userInfo.get('dept_name', '')
        request.session['group_id'] = userInfo.get('group_id', '-1')
        request.session['group_name'] = userInfo.get('dept_name', '')
        request.session['post_name'] = userInfo.get('post_name', '')
        return True

    def bk_weixin_login(self, request, user, userInfo):
        """
        @summary: 微信端登录
        """
        super(IeodAccount, self).bk_login(request, user)

        # 登录成功后，记录session
        if userInfo is None:
            return True
        request.session['avatar'] = userInfo.get('avatar', '')
        return True

    def redirectReLogin(self, request, loginUrl='', redirectFieldName=REDIRECT_FIELD_NAME):
        """
        跳转到login页面
        @note: OA登录使用该方法，否则调用父类的方法
        """
        # 非开发环境则使用父类跳转
        if self._config.RUN_MODE != 'DEVELOP' and self._config.OA_LOGIN is False:
            return super(IeodAccount, self).redirectReLogin(request, loginUrl, redirectFieldName)

        # OA 登录则跳转到 login_page页面（本地开发和OA_LOGIN）
        if request.is_ajax():
            jumpUrl = "http://%s%saccounts/login_page/" % (request.get_host(), self._config.SITE_URL)
            return self._redirect_401(request, jumpUrl=jumpUrl)

        # 如果是开发环境， 跳tof登录
        loginUrl = self._config.PASSPORT_SERVICE_SIGNIN_URL
        callback_url = "http://%s%saccounts/login/?%s=%s" % (
            request.get_host(), self._config.SITE_URL, redirectFieldName, urllib.quote(request.build_absolute_uri()))
        return self._redirect_login(request, callback=callback_url, loginUrl=loginUrl, redirectFieldName="url")
