# -*- coding: utf-8 -*-
"""
请不要修改该文件
如果你需要对settings里的内容做修改，请在config\settings_custom.py 文件中 添加即可
"""
import os

from settings import RUN_MODE
from config.settings_develop import APP_CODE as APP_CODE_DEV, SECRET_KEY as SECRET_KEY_DEV,\
         DEV_SEC_AUTH, DEV_SEC_AUTH_CGIS

# 框架运行环境
RUN_VER = 'ieod'
# ==============================================================================
# APP 基本信息
# ==============================================================================
# APP 编码
APP_CODE = os.environ.get("BK_APP_CODE", APP_CODE_DEV)
# APP 密码 (数据库密码，MQ密码)
APP_PWD = os.environ.get("BK_APP_PWD", "")
# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("BK_SECRET_KEY", SECRET_KEY_DEV)

# APP本地静态资源目录
STATIC_URL = os.environ.get("BK_STATIC_URL", "/static/%s/" % APP_CODE)
# APP的url前缀, 不要修改. 如 "/your_app_code/", 在页面中使用
SITE_URL = os.environ.get("BK_SITE_URL", "/")
# APP 微信本地静态资源目录
WEIXIN_STATIC_URL = os.environ.get("BK_WEIXIN_STATIC_URL", "/s/%s/static/weixin/" % APP_CODE)
# APP的微信url
WEIXIN_SITE_URL = "%sweixin/" % SITE_URL
# celery 的消息队列（RabbitMQ）配置
BROKER_URL_ENV = os.environ.get('BK_BROKER_URL', '')
# 通知公告域名
PUSH_URL = os.environ.get('BK_PUSH_URL', 'http://push.o.oa.com/api/')

# logging目录
LOGGING_DIR_ENV = os.environ.get('BK_LOGGING_DIR', '/data/home/apps/applogs/%s' % APP_CODE)

DB_HOST_DFT = os.environ.get('BK_DB_HOST', "")
DB_PORT_DFT = os.environ.get('BK_DB_PORT', '')

# 测试环境配置
if RUN_MODE == 'TEST':
    # 平台 URL
    BK_URL = os.environ.get("BK_URL", "http://t.open.oa.com")
    # APP静态资源目录url
    REMOTE_STATIC_URL = os.environ.get("BK_REMOTE_STATIC_URL", '%s/static_api/' % BK_URL)
    # 平台微信URL
    WEIXIN_BK_URL = os.environ.get("BK_WEIXIN_BK_URL", "http://mt.bk.tencent.com")
    # 微信APP静态资源目录url
    WEIXIN_REMOTE_STATIC_URL = os.environ.get("BK_WEIXIN_REMOTE_STATIC_URL", '%s/static_api/' % WEIXIN_BK_URL)
    # 组件系统
    COMPONENT_SYSTEM_HOST = os.environ.get("BK_COMPONENT_SYSTEM_HOST", "http://t.open.oa.com/component")
# 正式环境配置
elif RUN_MODE == 'PRODUCT':
    # 平台 URL
    BK_URL = os.environ.get("BK_URL", "http://open.oa.com")
    # APP静态资源目录url
    REMOTE_STATIC_URL = os.environ.get("BK_REMOTE_STATIC_URL", '%s/static_api/' % BK_URL)
    # 平台微信URL
    WEIXIN_BK_URL = os.environ.get("BK_WEIXIN_BK_URL", "http://m.bk.tencent.com")
    # 微信APP静态资源目录url
    WEIXIN_REMOTE_STATIC_URL = os.environ.get("BK_WEIXIN_REMOTE_STATIC_URL", '%s/static_api/' % WEIXIN_BK_URL)
    # 组件系统
    COMPONENT_SYSTEM_HOST = os.environ.get("BK_COMPONENT_SYSTEM_HOST", "http://open.oa.com/component")
# 本地开发环境
else:
    # APP 微信本地静态资源目录
    WEIXIN_STATIC_URL = '%sweixin/' % STATIC_URL
    # 平台微信URL
    WEIXIN_BK_URL = "http://mt.bk.tencent.com"
    # 微信APP静态资源目录url
    WEIXIN_REMOTE_STATIC_URL = "%s/static_api/" % WEIXIN_BK_URL

# ===============================================================================
# 外部系统地址
# ===============================================================================
# 敏感权限管理系统，auth.cm.com
SEC_AUTH = os.environ.get('BK_SEC_AUTH', DEV_SEC_AUTH)
SEC_AUTH_CGIS = os.environ.get('BK_SEC_AUTH_CGIS', DEV_SEC_AUTH_CGIS)
