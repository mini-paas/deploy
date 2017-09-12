# -*- coding: utf-8 -*-

'''
API for tof,include:敏感权限系统相关，其他

#CheckSession说明----------------------------------------------------------
    使用login_required登录OA后, 第一次tof check_session时的结果:
    Result: (Result){
       status = 201
       status_info = "user don't login"
       auth_cm_com_session_key = None
       user_name = None
       login_url = "http://10.177.151.158/login/login.php?sys_id=558&login_mode=oa&"+
                    "sys_url=http%3A%2F%2Flocalhost%3A8000%2Ftest_app_tof%2Fpage_check_session%2F"
       auth_apply_url = None
     }
    上面的login_url是敏感系统的登录页,它首先转向oa登录,然后获取ticket后生成auth_cm_com_ticket,
    然后再模仿oa登录, 返回到你的url(不同的是后面了加上那个参数)
    然后你的url后台view里加入了auth_xxx_ticket再次请求checksession, 这次就成功了.
#----------------------------------------------------------
'''
import json

import httplib2
from suds.client import Client
from django.conf import settings

from common.log import logger
from app_control.models import Function_controller

# 敏感权限功能开关
tof_disabled = not settings.ENABLE_SEC_AUTH


def check_session(request):
    """
    CheckSession for tof
    @return (0/1/2, message)
            如:(0, 'check success') / (1, redirect_url) / (2, error_message)
    """
    if tof_disabled:
        return (0, u"check success")

    # 组装参数
    kwargs = _contruct_params(request)
    logger.info(u"敏感权限的验证参数: %s" % json.dumps(kwargs))
    result = ''
    try:
        # 调用远程接口
        soap_client = Client(settings.SEC_AUTH)
        result = soap_client.service.CheckSession(kwargs)
        if result.status == 0:
            # 成功, 保存信息到session
            request.session['key'] = result.auth_cm_com_session_key
            request.session['user_name'] = result.user_name
            logger.info(u"auth result: %s" % result)
            return (0, u"check success")
        return _handle_tof_error(result)
    except Exception as e:
        logger.error(u"敏感权限系统CheckSession接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统CheckSession接口出现异常: %s" % e)


def check_role(request, role_list):
    """
    check_biz_role的简化版(只检查角色), 参数role_list为角色命令字的list
    """
    return check_role(request, [(0, role) for role in role_list])


def check_biz_role(request, biz_role_list):
    """
    @summary: (业务-角色)权限接口(CheckBusinessRole), 检测是否是某个业务的角色
    @param biz_role_list (游戏id, 角色命令字)元组的列表，每个元组表示争对某个游戏id的某个角色
    @return (0/1/2, message)
            #如下: (0, [True,False,...]列表) / (1, redirect_url) / (2, error_message)
            #注意: 0只是表示请求成功, 并不表示检查权限有效
    """
    if tof_disabled:
        return (0, [True for i in biz_role_list])

    # 组装参数
    biz_role_relations = _pack_biz_role_list(biz_role_list)  # 把元组装换成字典
    kwargs = _contruct_params(request)
    kwargs['business_role_relation_list'] = biz_role_relations  # <角色命令字,游戏id> 列表
    kwargs.pop('auth_cm_com_ticket')  # 新接口存在技术性限制，传入此参数会导致错误

    try:
        # 调用远程Soap接口
        soap_client = Client(settings.SEC_AUTH)
        result = soap_client.service.CheckBusinessRole(kwargs)
        if result.status == 0:
            # 请求成功，返回检查结果列表
            return (0, result.check_result_list)
        return _handle_tof_error(result)
    except Exception as e:
        logger.error(u"敏感权限系统CheckBusinessRole接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统CheckBusinessRole接口出现错误: %s" % e)


def check_auth(request, operation_id):
    """
    Description: 检查用户是否拥有某操作的权限
    @param operation_id 操作的id
    @return: (0/1/2, message)
            #如下: (0, 'CheckAuth Success.') / (1, redirect_url) / (2, error_message)
    """
    if tof_disabled:
        return (0, 'CheckAuth Success.')

    kwargs = _contruct_params(request)
    kwargs['operation_id'] = operation_id  # 操作ID

    # 向鉴权系统发送验证请求
    try:
        soap_client = Client(settings.SEC_AUTH)
        result = soap_client.service.CheckAuth(kwargs)
        if result.status == 0:
            return (0, 'CheckAuth Success.')
        return _handle_tof_error(result)
    except Exception, e:
        logger.error(u"敏感权限系统CheckAuth接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统CheckAuth接口出现错误: %s" % e)


def check_auth_by_id_list(request, operation_id_list):
    """
    @summary: 检查用户是否拥有多个操作ID的权限
    @param operation_id_list 操作ID列表
    @return (0/1/2, message)
            #如下 (0, [True,False,...]列表)
                  (1, check_result_list)
                  (2, error_message)
    """
    return _check_auth_by_list('id', request, operation_id_list)


def check_auth_by_cmd_list(request, operation_command_list):
    """
    @summary: 检查用户是否拥有多个操作命令字的权限
    @param operation_command_list 操作命令字列表
    @return (0/1/2, message)
            #如下 (0, [True,False,...]列表)
                  (1, check_result_list)
                  (2, error_message)
    """
    return _check_auth_by_list('cmd', request, operation_command_list)


def _check_auth_by_list(cmd_or_id, request, operation_list):
    """
    @summary: 内部方法:检查用户是否拥有多个操作的权限 (根据命令字或id)
    @param cmd_or_id: 两种指定操作的方式, 通过命令字或者id
                      'cmd':指定operation_list必须是命令字列表
                      'id' :指定id_list必须是id列表
    @return (0/1/2, message)
            #如下 (0, [True,False,...]列表)
                  (1, check_result_list)
                  (2, error_message)
    """
    if tof_disabled:
        return (0, [True for i in operation_list])

    # 组装参数
    kwargs = _contruct_params(request)
    if cmd_or_id == 'cmd':
        kwargs['operation_command_list'] = operation_list
    elif cmd_or_id == 'id':
        kwargs['operation_id_list'] = operation_list
    kwargs.pop('auth_cm_com_ticket')  # 新接口存在技术性限制，传入此参数会导致错误

    try:
        # 调用远程Soap接口CheckBusinessRole
        soap_client = Client(settings.SEC_AUTH)
        if cmd_or_id == 'cmd':
            result = soap_client.service.CheckAuthByCommandList(kwargs)
        elif cmd_or_id == 'id':
            result = soap_client.service.CheckAuthByIDList(kwargs)
        if result.status == 0:
            # 请求成功，返回检查结果列表
            return (0, result.check_result_list)
        return _handle_tof_error(result)
    except Exception as e:
        logger.error(u"敏感权限系统CheckAuthByList接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统出现错误: %s" % e)


def write_operation_record(request, operation_id, kwargs_operation_log):
    """
    WriteOperationRecord record for tof
    @param operation_id: 敏感系统的operation_id
    @param kwargs_operation_log: kwargs_operation_log的详细参数
                                        {
                                            'op_name': u'操作名称',
                                            'op_time': u'操作时间',
                                            'op_user': u'操作人',
                                            'op_param': u'操作参数',
                                            'op_pattern': u'操作方式',
                                            'op_object': u'操作对象',
                                            'op_content': u'操作内容',
                                            'op_result': u'操作结果',
                                            'op_extend1': u'扩展1',
                                            'op_extend2': u'扩展2',
                                        }
    """
    # 检查参数kwargs_operation_log是不是字典
    if not isinstance(kwargs_operation_log, dict):
        return (3, u"""参数kwargs_operation_log必须是字典，格式为：{
                        'op_name': u'操作名称',
                        'op_time': u'操作时间',
                        'op_user': u'操作人',
                        'op_param': u'操作参数',
                        'op_pattern': u'操作方式',
                        'op_object': u'操作对象',
                        'op_content': u'操作内容',
                        'op_result': u'操作结果',
                        'op_extend1': u'扩展1',
                        'op_extend2': u'扩展2',
                    }""")
    # 组装参数
    operation_log = {
        'op_name': '',
        'op_time': '',
        'op_user': '',
        'op_param': '',
        'op_pattern': '',
        'op_object': '',
        'op_content': '',
        'op_result': '',
        'op_extend1': '',
        'op_extend2': '',
    }
    operation_log.update(kwargs_operation_log)
    kwargs = _contruct_params(request)
    kwargs.update({
        'system_id': settings.SEC_SYSTEM_ID,             # 敏感系统id
        'operation_id': operation_id,                    # 操作id
        'operation_log': "|".join(operation_log.values()).encode("utf-8"),   # 操作日志内容（UTF-8编码）
    })

    try:
        # 调用远程接口WriteOperationRecord
        soap_client = Client(settings.SEC_AUTH)
        result = soap_client.service.WriteOperationRecord(kwargs)
        if result.status == 0:
            # 成功
            return (0, u"write success")
        return _handle_tof_error(result)
    except Exception as e:
        logger.error(u"敏感权限系统WriteOperationRecord接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统WriteOperationRecord接口出现错误: %s" % e)


def add_operation(request, operation_list):
    """
    批量添加业务系统操作
    输入操作列表（系统id，操作名称，对应CGI列表，权限级别）
    输出 结果（Yes/No）操作id列表
    注意: 使用此接口需要3种授权：
    1. 敏感中系统ID的管理员
    2. IP授权
    3. 系统ID授权
    @param operation_list:
        [{"bu_sys_id":3,                               // 业务系统ID
          "operation_name":"",                        // 操作名称
          "operation_command":"",                     // 可选, 操作命令字
          "sec_class":3,                              // 操作级别
          "operation_cgi_list": [ "url1","url2" ..]   //对应CGI

         },
        ...]
    """
    kwargs = _contruct_params(request)
    kwargs.update({'data': operation_list})

    try:
        # 调用远程接口AddOperation
        result = _http_request_tof('AddOperation', 'POST', kwargs)
        if result['status_code'] == 0:
            # 成功
            return (0, u"add_operation success")
        return (2, result['status_info'])
    except Exception as e:
        logger.error(u"敏感权限系统AddOperation接口，请求出现异常: %s, kwargs:%s, result:%s" % (e, kwargs, result))
        return (2, u"[蓝鲸]调用敏感权限系统AddOperation接口出现错误: %s" % e)


def _handle_tof_error(result):
    """
    根据TOF返回的非成功状态码, 获取状态信息. 注:status=0的情况请自行处理
    @param result: tof soap返回的结果对象
    @return tuple(状态分类 0/1/2, 消息)
    """
    status = result.status
    status_info = result.status_info
    if 100 <= status < 200:
        # 服务不可用
        err_msg = u"[敏感权限系统]服务不可用,请等待数秒后重试,如还是错误，请联系管理员! (status:%s, info:%s)" % (status, status_info)
        logger.error(err_msg)
        return (2, err_msg)
    elif 200 <= status < 300:
        # 登陆失败，需要重新登录
        logger.error(u"auth result: %s" % result)
        return (1, result.login_url)
    elif status == 301:
        # TODO:这个逻辑是否可以和300-400合并
        # 没有系统的访问权限（即用户一个权限都没有，不允许看到页面）。
        err_msg = u"[敏感权限系统]您没有系统的访问权限."
        logger.error(err_msg)
        return (2, err_msg)
    elif 300 <= status < 400:
        # 没有操作权限
        err_msg = u"[敏感权限系统]您的权限不足:%s." % result.status_info
        logger.error(err_msg)
        return (2, err_msg)
    else:
        # 未知异常
        logger.error(u"auth result: %s" % result)
        return (2, u"[敏感权限系统]未知错误,请联系管理员! (status:%s, info:%s)" % (status, status_info))


def _contruct_params(request):
    """
    @summary 从request里提取信息,构建TOF通用参数
    """
    session = request.session
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))  # 用户ip
    return {
        'user_name': session.get('user_name', ''),         # 用户名
        'auth_cm_com_session_key': session.get('key', ''),  # session key (用户的敏感登陆态标识)
        'user_url': request.build_absolute_uri(),          # 访问url
        'user_ip': user_ip,                                # 用户ip
        'auth_cm_com_ticket': request.GET.get('auth_cm_com_ticket', ''),  # 用户进行登陆动作时产生的敏感ticket
        'local_session_id': session.session_key,           # session_id (浏览器与业务系统之间会话的标识)
        'system_id': settings.SEC_SYSTEM_ID,               # 业务系统在TOF中的id
    }


def _http_request_tof(cgi_action, http_method, request_data):
    """
    @summary 对敏感权限系统的新cgi接口发起http请求(非SOAP API,而是restful webservice)
    @param http_method: GET/POST/PUT...
    @param request_data: 请求的数据dict
    @return 服务端传回的json对象
    """
    uri = '%s%s' % (settings.SEC_AUTH_CGIS, cgi_action)

    headers = {
        "Accept": "text/html",
        "User-Agent": "IE",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp, content = httplib2.Http().request(uri, http_method,
                                            json.dumps(request_data).encode('utf-8'), headers)

    if resp.status == 200:
        # 成功，返回content
        try:
            content_dict = json.loads(content)  # status_code, status_info
            return content_dict
        except Exception, e:
            logger.error(u"敏感权限系统返回数据格式不正确!%s" % e)
            return None
    else:
        logger.error(u"请求出现错误,错误状态：%s" % resp.status)
        return None


def _pack_biz_role_list(biz_role_list):
    """
    @summary: check_biz_role的帮助函数, 把(游戏id, 角色命令字)元组的列表转换成字典列表, 比如:
    @param:     [(121, '558_33')]
    @return:    [{'business_id': 121, 'role_command': '558_33'}]
    """
    return [{'business_id': game_id, 'role_command': role_command}
            for game_id, role_command in biz_role_list]


def func_check(func_code):
    """
    @summary: 检查功能是否开放
    @param func_code 功能ID
    @return (0/1/2/3, message)
            #如下 (0, No check)
                  (1, check success)
                  (2, check failed)
                  (3, error_message)
    """
    if settings.ENABLE_FUNC_AUTH:
        result = Function_controller.objects.func_check(func_code)
        if result['result']:
            if result['message']:
                return (1, 'check success')
            else:
                return (2, 'check failed')
        else:
            logger.error(u"check error,%s" % result['message'])
            return (3, 'check error,%s' % result['message'])
    return (0, 'No check')
