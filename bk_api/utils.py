# coding=utf-8
'''
公用方法: 发送http请求
'''
import json
import httplib2
from django.utils.http import urlencode
from bk_api.settings_bk import logger


def http_get_workbench(url, query=''):
    '''
    #对第一层L1工作台系统的Web服务的Http Get请求
    #响应格式规范为 {result:True/False, message:服务处理消息, data:服务返回数据}
    @param query: string,number,or a iterable obj
    @return: 请注意, 返回的是原始响应数据中的data字段
    '''
    # 如果是一个iterable，则转换成url的param字符串
    if hasattr(query, 'items'):
        query = urlencode(query)
    uri = '%s?%s' % (url, query) if query else url
    resp, content = httplib2.Http().request(uri, 'GET')
    if resp.status == 200:
        # 成功，返回content
        try:
            content_dict = json.loads(content)
            if not content_dict['result']:
                logger.error(content_dict['message'])
            return content_dict['data']
        except:
            logger.error(u"返回数据格式不正确，统一为json")
            return None
    else:
        logger.error(u"请求出现错误,错误状态：%s" % resp.status)
        return None


def http_request_workbench(url, http_method, query=''):
    '''
            发起GET/POST等各种请求
    @param query: string,number,or a iterable obj
    @param http_method: GET/POST等各种请求方式
    @note: httplib2的post里的数据值必须转成utf8编码
    @note: 优先选用django的querydict的urlencode, urllib的urlencode会出现编码问题。
    @note: 参照
    http://stackoverflow.com/questions/3110104/unicodeencodeerror-ascii-codec-cant-encode-character-when-trying-a-http-post
    @note: 请求参数query中的参数项如果是json, 请不要传入python dict, 一定要传入json字符串, 否则服务端将无法解析json(单双引号问题)
    @return: 直接返回原始响应数据(包含result,data,message的字典)
    '''
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
