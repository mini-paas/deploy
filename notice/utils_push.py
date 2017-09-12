# -*- coding: utf-8 -*-

import json
import datetime
import httplib2
import traceback

from django.utils.http import urlencode

from settings import APP_CODE, SECRET_KEY, PUSH_URL
from common.log import logger


# ===============================================================================
# 访问第三方接口的超时时间
TIME_OUT = 10
GET_ALL_NOTICES = '%sget/all' % PUSH_URL
GET_UNREAD_NOTICES_URL = '%sget/unread_notices' % PUSH_URL

# 通知中心的 app_code 需要添加前缀
N_APP_CODE = 'bkapp_t_%s' % APP_CODE
APP_SECERT = SECRET_KEY
# ===============================================================================


def _get_user_notread_notice(username):
    """
    获取用户的未读的通知消息
    """
    query = {
        'username': username,
        'app_code': N_APP_CODE,
        'app_secert': APP_SECERT
    }
    try:
        # 记录接口调用时间
        _start = datetime.datetime.now()
        # 本地开发不访问 通知公告接口
        content = http_request_common(GET_UNREAD_NOTICES_URL, 'GET', query, TIME_OUT) if PUSH_URL else {}
        _end = datetime.datetime.now()
        _time = _end - _start
        _delay = _time.days * 24 * 60 * 60 * 1000 + _time.seconds * 1000 + _time.microseconds / 1000  # 计算时间差到ms
        _delay = int(_delay)
        if _delay > 500:
            logger.info(u"公告接口 _get_user_notread_notice 接口调用时长:%s ms,query:%s" % (_delay, query))
    except Exception, e:
        logger.error(u"获取用户未读公告 _get_user_notread_notice 异常：%s" % e)
        content = {}

    # 解析返回的接口数据
    data = content.get('data', {}) if content else {}
    data = data or {}
    num = data.get('num', 0)
    notices = data.get('notices', [])

    return num, notices


def _get_all_notice():
    """
    获取App的所有通知消息
    """
    query = {
        'app_code': N_APP_CODE,
        'app_secert': APP_SECERT
    }
    try:
        # 记录接口调用时间
        _start = datetime.datetime.now()
        # 本地开发不访问 通知公告接口
        content = http_request_common(GET_ALL_NOTICES, 'GET', query, TIME_OUT) if PUSH_URL else {}
        _end = datetime.datetime.now()
        _time = _end - _start
        _delay = _time.days * 24 * 60 * 60 * 1000 + _time.seconds * 1000 + _time.microseconds / 1000  # 计算时间差到ms
        _delay = int(_delay)
        if _delay > 500:
            logger.info(u"公告接口 get_all_notice 接口调用时长:%s ms,query:%s" % (_delay, query))
    except Exception, e:
        logger.error(u"获取应用所有公告 get_all_notice 异常：%s" % e)
        content = {}
    # 解析返回的接口数据
    data = content.get('data', {}) if content else {}
    return data


def http_request_common(url, http_method, query='', timeout=None, headers=None):
    '''
    @summary: 发起GET/POST等各种请求
    @param query: string,number,or a iterable obj
    @param http_method: GET / POST  等各种请求方式
    @return: 直接返回原始响应数据(包含result,data,message的字典)
    '''
    # 如果是一个iterable，则转换成url的param字符串
    if hasattr(query, 'items'):
        query = urlencode(query)
    if http_method == 'POST':
        if headers:
            resp, content = httplib2.Http(timeout=timeout).request(url, http_method, body=query, headers=headers)
        else:
            resp, content = httplib2.Http(timeout=timeout).request(url, http_method, body=query)
    else:
        uri = '%s?%s' % (url, query) if query else url
        resp, content = httplib2.Http(timeout=timeout).request(uri, 'GET')
    if resp.status == 200:
        # 成功，返回content
        try:
            content_dict = json.loads(content)
            return content_dict
        except Exception, e:
            log_message = u"返回数据格式不正确，统一为json.\n uri：%s, content:%s.\n Exception: %s\n===>traceback format_exc: %s" % (
                uri, content, e, traceback.format_exc())
            logger.error(log_message)
            return {'result': False, 'message': u"调用远程服务失败，Http请求返回数据格式错误!"}
    else:
        log_message = u"调用远程服务失败，Http请求错误状态码：%s\n%s\nurl:%s\nquery:%s" % (
            resp.status, http_method, url, query)
        logger.error(log_message)
        return {'result': False, 'message': u"调用远程服务失败，Http请求错误状态码：%s" % resp.status}
