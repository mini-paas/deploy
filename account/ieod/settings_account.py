# -*- coding: utf-8 -*-
"""
登录相关的配置
"""
import os

from django.conf import settings

from account.settings_account import *
try:
    from config.settings_custom import OA_LOGIN
except:
    OA_LOGIN = False

DEV_LOGIN_URL = 'http://login.o.oa.com/'  # 登录页面链接
DEV_PLAIN_LOGIN_URL = 'http://login.o.oa.com/plain/'  # 登录页面弹窗

LOGIN_URL = os.environ.get('BK_LOGIN_URL', DEV_LOGIN_URL)
PLAIN_LOGIN_URL = os.environ.get('BK_PLAIN_LOGIN_URL', DEV_PLAIN_LOGIN_URL)

IS_LOGIN_URL = '%suser/is_login' % LOGIN_URL
GET_INFO_URL = '%suser/get_info' % LOGIN_URL  # 蓝鲸统一登录获取用户信息
GET_FULL_INFO = '%suser/get_full_info' % LOGIN_URL  # 蓝鲸统一登录获取用户详情

# ===============================================================================
# TOF OA登录相关
# ===============================================================================
# 本地开发
DEV_PASSPORT_SERVICE_SIGNIN_URL = 'http://login.oa.com/modules/passport/signin.ashx'
DEV_PASSPORT_SERVICE_SIGNOUT_URL = 'http://login.oa.com/modules/passport/signout.ashx'
# TOF 登录票据校验接口
DEV_PASSPORT_SERVICE_WSDL = 'http://login.oa.com/services/passportservice.asmx?WSDL'

# 正式运行时从环境变量中获取
PASSPORT_SERVICE_SIGNIN_URL = os.environ.get('BK_PASSPORT_SERVICE_SIGNIN_URL', DEV_PASSPORT_SERVICE_SIGNIN_URL)
PASSPORT_SERVICE_SIGNOUT_URL = os.environ.get('BK_PASSPORT_SERVICE_SIGNOUT_URL', DEV_PASSPORT_SERVICE_SIGNOUT_URL)
# TOF 登录票据校验接口
PASSPORT_SERVICE_WSDL = os.environ.get('BK_PASSPORT_SERVICE_WSDL', DEV_PASSPORT_SERVICE_WSDL)

# 微信相关
WEIXIN_BK_URL = settings.WEIXIN_BK_URL
# 微信登录接口
WEIXIN_GET_INFO_URL = LOGIN_URL + 'user/weixin/get_user_info/?code=%s'
WEIXIN_LOGIN_URL = settings.SITE_URL + 'weixin/accounts/login/'
WEIXIN_URL_PREFIX = settings.SITE_URL + 'weixin/'
# 跳转到微信重定向链接
DEV_WEIXIN_OAUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
WEIXIN_OAUTH_URL = os.environ.get('BK_WEIXIN_OAUTH_URL', DEV_WEIXIN_OAUTH_URL)
WEIXIN_APP_ID = os.environ.get('BK_WEIXIN_APP_ID', 'wxab249edd27d57738')
