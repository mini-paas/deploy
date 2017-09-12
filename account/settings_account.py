# -*- coding: utf-8 -*-

"""
登录相关的配置
"""
from django.conf import settings
# ===============================================================================
# Djagno 运行环境变量
# ===============================================================================
APP_CODE = settings.APP_CODE
RUN_VER = 'ieod'

# ===============================================================================
# 系统配置
# ===============================================================================
BK_URL = settings.BK_URL
SITE_URL = settings.SITE_URL

# ===============================================================================
# 超时时间
# ===============================================================================
TIME_OUT = 10

# ===============================================================================
# 登录链接设置
# ===============================================================================
LOGIN_URL = SITE_URL + 'accounts/login/'  # 登录页面链接
PLAIN_LOGIN_URL = SITE_URL + 'accounts/login/'  # 登录页面弹窗
LOGOUT_URL = SITE_URL + 'accounts/logout/'  # 登出url
IS_LOGIN_URL = '%suser/is_login' % LOGIN_URL
GET_INFO_URL = '%suser/get_info' % LOGIN_URL  # 蓝鲸统一登录获取用户信息
GET_FULL_INFO = '%suser/get_full_info' % LOGIN_URL  # 蓝鲸统一登录获取用户详情
LOGIN_REDIRECT_URL = SITE_URL  # 登录后跳转

# ===============================================================================
# 登录页面模板
# ===============================================================================
LOGIN_PAGE_TEMPLATE = '/account/login_page.html'
LOGIN_SUCCESS_TEMPLATE = '/account/login_success.html'
LOGIN_FAIL_TEMPLATE = '/account/login_fail.html'
# 微信登录失败页面模版
WEIXIN_LOGIN_FAIL_TEMPLATE = '/account/weixin_login_fail.html'
# ==============================================================================
# APP 运行环境配置信息
# ==============================================================================
# 此处WSGI_ENV设置用于正式环境部署
WSGI_ENV = settings.WSGI_ENV
RUN_MODE = settings.RUN_MODE

# ===============================================================================
# 日志配置
# ===============================================================================
from common.log import logger