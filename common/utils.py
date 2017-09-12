# -*- coding: utf-8 -*-
'''
蓝鲸平台提供的公用方法

#===============================================================================
# 1.页面输入内容转义（防止xss攻击）
from common.utils import html_escape, url_escape

 # 转义html内容
 html_content = html_escape(input_content)

 # 转义url内容
 url_content = url_escape(input_content)
#===============================================================================
'''
from blueking.component.ieod.shortcuts import get_client_by_request

from common.pxfilter import XssHtml


def html_escape(str_escape, fromtype=0, is_json=False):
    """
    字符串转义为html代码
    @param str_escape: 需要解析的html代码
    @param fromtype: 来源，0：views函数，1：middleware
    @param is_json: 是否为json串
    """
    try:
        result_str = escape_new(str_escape, fromtype, is_json)
        return result_str
    except Exception:
        return str_escape


def url_escape(url_escape):
    """
    转义url中的特殊字符
    @param str_escape: 需要解析的url
    """
    try:
        result_str = escape_url(url_escape)
        return result_str
    except Exception:
        return url_escape


def html_escape_name(str_escape):
    """
    字符串转义为html代码
    @param str_escape: 需要解析的html代码
    """
    try:
        result_str = escape_name(str_escape)
        return result_str
    except Exception:
        return str_escape


def escape_url(s):
    s = s.replace("<", "")
    s = s.replace(">", "")
    s = s.replace(' ', "")
    s = s.replace('"', "")
    s = s.replace("'", "")
    return s


def escape_name(s):
    '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated.
    rewrite the cgi method
    '''
    s = s.replace("&", "")  # Must be done first!
    s = s.replace("<", "")
    s = s.replace(">", "")
    s = s.replace(' ', "")
    s = s.replace('"', "")
    s = s.replace("'", "")
    return s


def check_script(str_escape, fromtype=0):
    """
    防止js脚本注入
    @param str_escape: 要检测的字符串
    @param fromtype: 0：views，1：middleware
    """
    try:
        parser = XssHtml()
        parser.feed(str_escape)
        parser.close()
        return parser.getHtml()
    except Exception:
        return str_escape


def escape_new(s, fromtype, is_json):
    '''Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated.
    rewrite the cgi method
    @param fromtype: 来源，0：views函数，1：middleware（对&做转换），默认是0
    @param is_json: 是否为json串（True/False） ，默认为False
    '''
    # &转换
    if fromtype == 1 and not is_json:
        s = s.replace("&", "&amp;")  # Must be done first!
    # <>转换
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    # 单双引号转换
    if not is_json:
        s = s.replace(' ', "&nbsp;")
        s = s.replace('"', "&quot;")
        s = s.replace("'", "&#39;")
    return s


def chek_right_by_cc(request, username, biz_cc_id, cc_name_list):
    """
    @summary:  根据业务id判断用户是否有指定的权限
    @param cc_name_list: 权限在cc中字段列表，如 ['Maintainers', 'PmpProductMan']
    @return: True/False
    """
    res = False
    client = get_client_by_request(request)
    cc_res = client.cc.get_application_staff({'app_id': biz_cc_id})
    app_info_list = cc_res.get('data', [])
    # cc接口返回的是一个列表，取第一项的值
    app_info = app_info_list[0] if app_info_list else {}
    if app_info:
        for cc_name in cc_name_list:
            user_list = app_info.get(cc_name).split(';') if app_info.get(cc_name) else []
            # 用户具有该项权限则直接返回 True
            if username in user_list:
                res = True
                break
    return res
