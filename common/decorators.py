# -*- coding: utf-8 -*-

"""
装饰器
1.权限pad装饰器，permission_required(已经写好装饰器，可自行定义验证逻辑)
"""
from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.shortcuts import redirect

from config.settings_env import SITE_URL
from common.tof import check_session, check_biz_role, check_auth,\
    check_auth_by_id_list, check_auth_by_cmd_list
from common.log import logger
from common.utils import chek_right_by_cc

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


# ===============================================================================
# 转义装饰器
# ===============================================================================
def escape_exempt(view_func):
    """
    转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_script(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行javascript escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_script = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_url(view_func):
    """
    被此装饰器修饰的action会对GET与POST参数进行url escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_url = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def escape_exempt_param(*param_list, **param_list_dict):
    """
    此装饰器用来豁免某个view函数的某个参数
    @param param_list: 参数列表
    @return:
    """
    def _escape_exempt_param(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        if param_list_dict.get('param_list'):
            wrapped_view.escape_exempt_param = param_list_dict['param_list']
        else:
            wrapped_view.escape_exempt_param = list(param_list)
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return _escape_exempt_param


# ==============================================================================
# 权限判断装饰器
# ==============================================================================
# 判断当前登录用户是否 有指定业务的权限
# 权限参数，根据实际情况填写
BIZ_CC_ID = ''  # 业务在cc中的id
CC_NAWM_LIST = ['Maintainers']  # 权限在cc中字段列表 , Maintainers表示运维


def permission_required(app_code):
    """
    Decorator for views that checks whether a user has a particular permission
    to access the app_code, redirecting to the 403 page if necessary.
    Unused.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            username = request.user.username
            res = chek_right_by_cc(request, username, BIZ_CC_ID, CC_NAWM_LIST)
            # TODO 调用判断权限的方法
            if res:
                return view_func(request, *args, **kwargs)
            # 权限不足提示页面，可根据实际情况修改
            return _redirect_403(request)

        return _wrapped_view
    return decorator


# ==============================================================================
# tof_check_session 检查会话
# ==============================================================================
def tof_check_session(view_func):
    """
    Decorator for views that checks session for tof.
    """
    def _wrapped_view(request, *args, **kwargs):
        _result, message = check_session(request)
        if _result == 0:
            # 成功
            return view_func(request, *args, **kwargs)
        logger.error(u"错误码：%s, 错误消息：%s, 是否是ajax请求：%s" % (_result, message, request.is_ajax()))
        return _response_for_failure(request, _result, message, request.is_ajax())
    return _wrapped_view


# ==============================================================================
# tof_check_biz_role <游戏-角色>鉴权
# ==============================================================================
def tof_check_biz_role(biz_role_list):
    """
    判断是否为某个游戏的特定角色, 需要传入参数：(游戏id, 角色命令字)元组的list
    此处判断所有业务角色有效，否则跳转至无权限页面
    @param biz_role_list: 如[(121, '558_1') , (120, '558_1') ]
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, message = check_biz_role(request, biz_role_list)
            if _result == 0:
                # 成功，biz_role中有一个无权限，则不能通过
                for valid_biz_role in message:
                    if not valid_biz_role:
                        # TODO:找出不符合的角色的详细信息
                        return _redirect_403(request)
                return view_func(request, *args, **kwargs)
            return _response_for_failure(request, _result, message, request.is_ajax())
        return _wrapped_view
    return decorator


def tof_check_role(role_list):
    """
    单独检查角色 (tof_check_biz_role的简化版)
    @param role_list: 角色命令字的列表, 如['558_developer', '558_user']
    """
    return tof_check_biz_role([(0, role) for role in role_list])


# ==============================================================================
# tof_check_auth装饰器：操作鉴权
# ==============================================================================
def tof_check_auth(operation_id):
    """
    Decorator for views that checks session for tof.
    @param operation_id: action
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, message = check_auth(request, operation_id)
            if _result == 0:
                # 成功
                return view_func(request, *args, **kwargs)
            return _response_for_failure(request, _result, message, request.is_ajax())
        return _wrapped_view
    return decorator


# ==============================================================================
# tof_check_auth装饰器：操作鉴权
# ==============================================================================
def tof_check_auth_by_id_list(operation_id_list):
    """
    Decorator for views that checks session for tof.
    @param operation_id_list: 操作ID列表
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, message = check_auth_by_id_list(request, operation_id_list)
            if _result == 0:
                # 请求成功，列表中有一个无权限，则不能通过
                for valid_op in message:
                    if not valid_op:
                        # TODO:找出不符合的操作的详细信息
                        return _redirect_403(request)
                return view_func(request, *args, **kwargs)
            return _response_for_failure(request, _result, message, request.is_ajax())
        return _wrapped_view
    return decorator


# ==============================================================================
# tof_check_auth装饰器：操作鉴权
# ==============================================================================
def tof_check_auth_by_cmd_list(operation_command_list):
    """
    Decorator for views that checks session for tof.
    @param operation_command_list: 操作命令字列表
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, message = check_auth_by_cmd_list(request, operation_command_list)
            if _result == 0:
                # 请求成功，列表中有一个无权限，则不能通过
                for valid_op in message:
                    if not valid_op:
                        # TODO:找出不符合的角色的详细信息
                        return _redirect_403(request)
                return view_func(request, *args, **kwargs)
            return _response_for_failure(request, _result, message, request.is_ajax())
        return _wrapped_view
    return decorator


def _response_for_failure(request, _result, message, is_ajax):
    """
    内部通用方法: 请求敏感权限出错时的处理(1和2)
    @param _result: 结果标志位
    @param message: 结果信息
    @param is_ajax: 是否是ajax请求
    """
    if _result == 1:
        # 登陆失败，需要重新登录,跳转至登录页
        if is_ajax:
            return HttpResponse(status=402)
        return redirect(message)
    elif _result == 2:
        # error(包括exception)
        return _redirect_403(request)


def _redirect_403(request):
    """
    转到403权限不足的提示页面
    """
    url = SITE_URL + 'accounts/check_failed/?code=403'
    if request.is_ajax():
        resp = HttpResponse(status=403, content=url)
        return resp
    return redirect(url)
