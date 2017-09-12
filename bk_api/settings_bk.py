# -*- coding: utf-8 -*-
"""
bk_api 全局常量配置
"""
import os
import logging

# ===============================================================================
# 系统配置
# ===============================================================================
# 蓝鲸平台地址（本地开发 ）
DEV_BK_URL = "http://t.open.oa.com"
# 蓝鲸平台地址（正式运行时从环境变量中获取）
BK_URL = os.environ.get("BK_URL", DEV_BK_URL)
# APP 的url前缀, 不要修改. 如 "/s/your_app_code/", 在页面中使用
SITE_URL = os.environ.get("BK_SITE_URL", "/")


# ==============================================================================
# APP 运行环境配置信息
# ==============================================================================
# 此处WSGI_ENV设置用于正式环境部署
WSGI_ENV = os.environ.get("DJANGO_CONF_MODULE", "")
RUN_MODE = 'DEVELOP'    # DEVELOP TEST PRODUCT
if WSGI_ENV.endswith("production"):
    RUN_MODE = "PRODUCT"
elif WSGI_ENV.endswith("testing"):
    RUN_MODE = "TEST"
else:
    RUN_MODE = "DEVELOP"

# ===============================================================================
# 日志配置
# ===============================================================================
# 用于组件调用的日志记录， 配合settings的LOGGING属性
logger = logging.getLogger('root')
