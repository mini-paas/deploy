# -*- coding: utf-8 -*-
"""
account的一些公用方法
"""

import urlparse
import json
import httplib2

from django.utils.http import urlencode

from common.log import logger


def http_referer(request):
    """
    获取 HTTP_REFERER 头
    """

    if 'HTTP_REFERER' in request.META:
        http_referer = urlparse.urlparse(request.META['HTTP_REFERER'])[2]
    else:
        from account.factories import AccountFactory
        account = AccountFactory.getAccountObj()
        http_referer = account._config.LOGIN_REDIRECT_URL
    return http_referer


def http_request_workbench(url, http_method, query=''):
    """
    发起GET/POST等各种请求
    @param query: string,number,or a iterable obj
    @param http_method: GET/POST等各种请求方式
    @note: httplib2的post里的数据值必须转成utf8编码
    @note: 优先选用django的querydict的urlencode, urllib的urlencode会出现编码问题。
    @note: 参照
    http://stackoverflow.com/questions/3110104/unicodeencodeerror-ascii-codec-cant-encode-character-when-trying-a-http-post
    @note: 请求参数query中的参数项如果是json, 请不要传入python dict, 一定要传入json字符串, 否则服务端将无法解析json(单双引号问题)
    @return: 直接返回原始响应数据(包含result,data,message的字典)
    """
    # 如果是一个iterable，则转换成url的param字符串
    if hasattr(query, 'items'):
        query = urlencode(query)
    if http_method == 'POST':
        resp, content = httplib2.Http().request(url, http_method, body=query)
    else:
        uri = '%s?%s' % (url, query) if query else url
        resp, content = httplib2.Http().request(uri, 'GET')
    if resp.status == 200:
        # 成功，返回content
        try:
            content_dict = json.loads(content)
            return content_dict
        except:
            logger.error(u"请求返回数据格式错误!")
            return {'result': 0, 'message': u"调用远程服务失败，Http请求返回数据格式错误!"}
    else:
        err = u"调用远程服务失败，Http请求错误状态码：%s" % resp.status
        logger.error(err)
        return {'result': 0, 'message': err}
