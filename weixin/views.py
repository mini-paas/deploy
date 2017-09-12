# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from blueking.component.ieod.shortcuts import get_client_by_request

from bk_api.task_api import remote_get_tasks
from common.log import logger
from common.mymako import render_mako_context
from weixin.core.api import WeiXinApi
from weixin.utils import is_weixin_visit


def index(request):
    """
    @summary: 业务数据页面
    """
    return render_mako_context(request, '/weixin/index.html', {})


def task_data_page(request):
    """
    @summary: 任务数据页面
    """
    return render_mako_context(request, '/weixin/task_data_page.html', {})


def share_template(request):
    """
    微信js-sdk样例页面
    """
    ctx = {}
    js_sign = {}
    # 判断是否为微信端访问
    is_weixin_terminal = is_weixin_visit(request)
    # 非微信端访问无法测试微信js-sdk相关功能
    if is_weixin_terminal:
        weixin_api = WeiXinApi()
        js_sign_result = weixin_api.get_js_sign(request.build_absolute_uri(), request.method)
        js_sign = js_sign_result.get('data')
    ctx = {'is_weixin_terminal': is_weixin_terminal, 'js_sign': js_sign}
    return render_mako_context(request, '/weixin/share_template.html', ctx)


def get_biz_histogram_data(request):
    """
    @summary: 业务星级数据统计柱状图数据
    """
    try:
        username = request.user.username
        client = get_client_by_request(request)
        result = client.cc.get_app_list_by_name({'name': username})['data']
        data_dict = {}
        data = {'categories': [], 'data': []}
        for i in result:
            if i['BipGradeName'] not in data_dict:
                data_dict[i['BipGradeName']] = 0
            data_dict[i['BipGradeName']] += 1
        for k in data_dict:
            star = u"其他" if k == '' or k is None else k
            data['categories'].append(star)
            data['data'].append(data_dict[k])
    except Exception, e:
        logger.error(u"获取数据出错：%s" % e)
        data = {'categories': [], 'data': []}
    return HttpResponse(json.dumps(data))


def get_biz_pie_data(request):
    """
    @summary: 业务星级数据统计饼图数据
    """
    try:
        username = request.user.username
        client = get_client_by_request(request)
        result = client.cc.get_app_list_by_name({'name': username})['data']
        data_dict = {}
        data = {'categories': [], 'data': []}
        for i in result:
            if i['BipGradeName'] not in data_dict:
                data_dict[i['BipGradeName']] = 0
            data_dict[i['BipGradeName']] += 1
        for k in data_dict:
            star = u"其他" if k == '' or k is None else k
            data['categories'].append(star)
            data['data'].append(
                {'name': star, 'value': data_dict[k]}
            )
        if not data['categories']:
            data = {'categories': [u"无业务"], 'data': [{'name': u"无业务", 'value': 1}]}
    except Exception, e:
        logger.error(u"获取数据出错：%s" % e)
        data = {'categories': [u"无业务"], 'data': [{'name': u"无业务", 'value': 1}]}
    return HttpResponse(json.dumps(data))


def task_histogram_data(request):
    """
    @summary: 任务数据统计柱状图数据
    """
    try:
        result = remote_get_tasks('app_template')
        data_list = result.get('message', [])
        data_dict = {}
        for i in data_list:
            if i['creator'] not in data_dict:
                data_dict[i['creator']] = 0
            data_dict[i['creator']] += 1
        data = {'categories': [], 'data': []}
        for k in data_dict:
            data['categories'].append(k)
            data['data'].append(data_dict[k])
    except Exception, e:
        logger.error(u"获取数据出错：%s" % e)
        data = {'categories': [], 'data': []}
    return HttpResponse(json.dumps(data))


def task_pie_data(request):
    """
    @summary: 任务数据统计饼图数据
    """
    try:
        result = remote_get_tasks('app_template')
        data_list = result.get('message', [])
        data_dict = {}
        data = {'categories': [], 'data': []}
        for i in data_list:
            if i['status_msg'] not in data_dict:
                data_dict[i['status_msg']] = 0
            data_dict[i['status_msg']] += 1
        for k in data_dict:
            data['categories'].append(k)
            data['data'].append(
                {'name': k, 'value': data_dict[k]}
            )
        if not data['categories']:
            data = {'categories': [u"无任务"], 'data': [{'name': u"无任务", 'value': 1}]}
    except Exception, e:
        logger.error(u"获取数据出错：%s" % e)
        data = {'categories': [u"无任务"], 'data': [{'name': u"无任务", 'value': 1}]}
    return HttpResponse(json.dumps(data))
