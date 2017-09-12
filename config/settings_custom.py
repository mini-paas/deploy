# -*- coding: utf-8 -*-
"""
用户自定义全局常量设置
"""
import os
from settings import RUN_MODE
from config.settings_env import APP_CODE, APP_PWD, DB_HOST_DFT, DB_PORT_DFT
# ==============================================================================
# 中间件和应用
# ==============================================================================
# 自定义中间件
MIDDLEWARE_CLASSES_CUSTOM = (
)
# 自定义APP
INSTALLED_APPS_CUSTOM = (
    # add your app here...
    'base',
    'nginx_deploy',
    'deploy',
    'rest_framework',
    'home_application',
    'weixin',
)

# ===============================================================================
# 静态资源
# ===============================================================================
# 静态资源文件(js,css等）在APP上线更新后, 由于浏览器有缓存, 可能会造成没更新的情况.
# 所以在引用静态资源的地方，都把这个加上，如：<script src="/a.js?v=${STATIC_VERSION}"></script>；
# 如果静态资源修改了以后，上线前改这个版本号即可
STATIC_VERSION = 2.0

# ===============================================================================
# CELERY 配置
# ===============================================================================
# APP是否使用celery
IS_USE_CELERY = False           # APP 中 使用 celery 时，将该字段设为 True
# TOCHANGE调用celery任务的文件路径, 即包含如下语句的文件： from celery import task
CELERY_IMPORTS = ()

# ===============================================================================
# 数据库设置 ，APP中使用外部数据库时可以在这里修改数据库设置
# APP 如果要使用蓝鲸内部其他APP的数据库 请rtx联系 【蓝鲸助手】
# ===============================================================================
DB_NAME = os.environ.get('BK_APP_CODE', APP_CODE)
DB_PWD = os.environ.get('BK_APP_PWD', APP_PWD)
# 数据库的配置信息
DB_HOST = os.environ.get('BK_DB_HOST', DB_HOST_DFT)
DB_PORT = os.environ.get('BK_DB_PORT', DB_PORT_DFT)

# 测试环境数据库设置
DATABASES_TEST = {
    # default 请不要做修改 ！！！！！！！！！！
    # 如要使用其他的数据库，请参考下面的注释添加，如有疑问，请 rtx联系 【蓝鲸助手】
    'default':
    {
        'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
        'NAME': DB_NAME,                             # 数据库名(与APP_CODE相同)
        'USER': DB_NAME,                              # 你的数据库user(与APP_CODE相同)
        'PASSWORD': DB_PWD,                       # 你的数据库password
        'HOST': DB_HOST,                               # APP数据库主机
        'PORT': DB_PORT,                               # APP数据库端口
    },
    #    # 使用了蓝鲸内部其他APP的数据库示例
    #    # OTHER_APP_CODE = os.environ.get('OTHER_APP_CODE', '')
    #    # OTHER_APP_PWD = os.environ.get('OTHER_APP_PWD', '')
    #    # 其中 OTHER_APP_CODE 和 OTHER_APP_PWD 环境变量请 rtx联系 【蓝鲸助手】添加
    #    'appcode_db':
    #    {
    #         'ENGINE': 'django.db.backends.mysql',
    #        'NAME': OTHER_APP_CODE,                              # 蓝鲸内部APP数据库名 （从环境变量中获取）
    #        'USER': OTHER_APP_CODE,                              # 蓝鲸内部APP数据库用户（与数据库名相同）
    #        'PASSWORD': OTHER_APP_PWD,                       # 蓝鲸内部APP数据密码 （从环境变量中获取）
    #        'HOST': DB_HOST,                                          # APP数据库主机
    #        'PORT': DB_PORT,                                           # APP数据库端口
    #    },
    #    # 使用外部数据库示例
    #    # 外部数据库授权，请 rtx联系 【蓝鲸助手】
    #    'external_db':
    #    {
    #         'ENGINE': 'django.db.backends.mysql',
    #        'NAME': '',                              # 外部数据库名
    #        'USER': '',                              # 外部数据库用户
    #        'PASSWORD': '',                     # 外部数据库密码
    #        'HOST': '',                             # 外部数据库主机
    #        'PORT': '',                             # 外部数据库端口
    #    },
}

# 正式环境数据库设置
DATABASES_PRODUCT = {
    # default 请不要做修改 ！！！！！！！！！！
    # 如要使用其他的数据库，请参考下面的注释添加，如有疑问，请 rtx联系 【蓝鲸助手】
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
        'NAME': DB_NAME,                             # 数据库名(默认与APP_CODE相同)
        'USER': DB_NAME,                              # 你的数据库user
        'PASSWORD': DB_PWD,                       # 你的数据库password
        'HOST': DB_HOST,                                # 不需要改动
        'PORT': DB_PORT,                                   # 不需要改动
    },
    #    # 使用了蓝鲸内部其他APP的数据库示例
    #    # OTHER_APP_CODE = os.environ.get('OTHER_APP_CODE', '')
    #    # OTHER_APP_PWD = os.environ.get('OTHER_APP_PWD', '')
    #    # 其中 OTHER_APP_CODE 和 OTHER_APP_PWD 环境变量请 rtx联系 【蓝鲸助手】添加
    #    'appcode_db':
    #    {
    #         'ENGINE': 'django.db.backends.mysql',
    #        'NAME': OTHER_APP_CODE,                              # 蓝鲸内部APP数据库名 （从环境变量中获取）
    #        'USER': OTHER_APP_CODE,                              # 蓝鲸内部APP数据库用户（与数据库名相同）
    #        'PASSWORD': OTHER_APP_PWD,                       # 蓝鲸内部APP数据密码 （从环境变量中获取）
    #        'HOST': DB_HOST,                                          # APP数据库主机
    #        'PORT': DB_PORT,                                           # APP数据库端口
    #    },
    #    # 使用外部数据库示例
    #    # 外部数据库授权，请 rtx联系 【蓝鲸助手】
    #    'external_db':
    #    {
    #         'ENGINE': 'django.db.backends.mysql',
    #        'NAME': '',                              # 外部数据库名
    #        'USER': '',                              # 外部数据库用户
    #        'PASSWORD': '',                     # 外部数据库密码
    #        'HOST': '',                             # 外部数据库主机
    #        'PORT': '',                             # 外部数据库端口
    #    },
}

# ===============================================================================
# 日志级别
# ===============================================================================
# 本地开发环境日志级别
LOG_LEVEL_DEVELOP = 'DEBUG'
# 测试环境日志级别
LOG_LEVEL_TEST = 'INFO'
# 正式环境日志级别
LOG_LEVEL_PRODUCT = 'ERROR'

# ===============================================================================
# 敏感系统设置
# ===============================================================================
# 敏感权限系统中的业务系统id
# TODO 如果开发者把这个id写错了，会不会出现问题？比如说批量添加操作的接口，需不需要什么其他限制来控制这个风险？
ENABLE_SEC_AUTH = False  # 是否开启敏感权限控制的功能开关, 若为False, 即使加了敏感权限代码也不会产生实际效果
SEC_SYSTEM_ID = 558    # 请自行在敏感权限系统中申请开通自己的业务系统，并在此处填上id。(558是蓝鲸开发模板系统的id, 仅用于开发测试)
ENABLE_FUNC_AUTH = True  # 是否开启功能检测的开关，若为False，则不检测功能是否可用

# ===============================================================================
# APP 执行流程
# ===============================================================================
# TOCHANGE 如果该APP需要调用第二层来执行任务，则这里就是任务引擎的事件执行流程的名字，
# 为方便管理请尽量配置的和APP_CODE一致
# 在这里定义:测试环境http://t.open.oa.com/circuit/admin/skewer/processdefinition/  (如没有权限，请联系huifu开通)
# 正式环境：http://open.oa.com/circuit/admin/skewer/processdefinition/
# 目前的模版工程里，只有一个EVENT_FLOW.
# 如果需要用多个，请配置成EVENT_FLOW_xxx, 并在你的前端代码里做出相应改动(context_processors.py, base.html)
# (测试用的模拟流程:app_template_v2)
EVENT_FLOW = 'app_template_v2'

# ===============================================================================
# 是否使用OA登录
# ===============================================================================
# 是否使用OA登录（如果APP需要oa登录的ticket， 则设置此项为True， 会使用OA登录而不是蓝鲸统一登录)
OA_LOGIN = False

RGW_ACCESS_KEY_ID = 'T06BP84NAPDF4L3LFUO8'
RGW_SECRET_ACCESS_KEY = 'Gf3QjecCgPVkoQbVM9OvaYBj8Jhf3PY2ynMUOgGq'

if RUN_MODE == 'PRODUCT':
    RGW_STORAGE_BUCKET_NAME = 'app-yw_deploy-prod'
else:
    RGW_STORAGE_BUCKET_NAME = 'app-yw_deploy-test'

RGW_ENDPOINT_URL = 'http://radosgw.open.oa.com/'
DEFAULT_FILE_STORAGE = 'bkstorages.backends.rgw.RGWBoto3Storage'
OAUTH_API_URL = 'http://apigw.o.oa.com'
OAUTH_COOKIES_PARAMS = {'rtx': 'bk_uid', 'bk_ticket': 'bk_ticket'}