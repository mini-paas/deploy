# -*- coding: utf-8 -*-
"""
context_processor for common(setting)

** 除setting外的其他context_processor内容，均采用组件的方式(string)
"""
from django.conf import settings
from account.settings_account import LOGIN_URL, LOGOUT_URL


def mysetting(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL,                                # MEDIA_URL
        'STATIC_URL': settings.STATIC_URL,                              # 本地静态文件访问
        'APP_PATH': request.get_full_path(),                            # 当前页面，url 路径
        'LOGIN_URL': LOGIN_URL,                                         # 登录链接
        'LOGOUT_URL': LOGOUT_URL,                                       # 登出链接
        'RUN_MODE': settings.RUN_MODE,                                  # 运行模式
        'APP_CODE': settings.APP_CODE,                                  # 在蓝鲸系统中注册的  "应用编码"
        'SITE_URL': settings.SITE_URL,                                  # URL前缀
        'REMOTE_STATIC_URL': settings.REMOTE_STATIC_URL,                # 远程静态资源url
        'STATIC_VERSION': settings.STATIC_VERSION,                      # 静态资源版本号,用于指示浏览器更新缓存
        'BK_URL': settings.BK_URL,                                      # 蓝鲸平台URL
        'CHINESE_NAME': request.session.get('chinese_name', ''),        # 用户中文名
        'DEPT_NAME': request.session.get('dept_name', ''),              # 用户部门
        'POST_NAME': request.session.get('post_name', ''),              # 用户小组
        'EVENT_FLOW': settings.EVENT_FLOW,                              # OVERFLOW 流程模版名称
        'WEIXIN_STATIC_URL': settings.WEIXIN_STATIC_URL,                # 微信页面本地静态文件url前缀
        'WEIXIN_SITE_URL': settings.WEIXIN_SITE_URL,                    # 微信页面 请求url前缀
        'WEIXIN_REMOTE_STATIC_URL': settings.WEIXIN_REMOTE_STATIC_URL,  # 微信页面远程静态资源url
    }
