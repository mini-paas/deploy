# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
from django.conf import settings

from config.urls_custom import urlpatterns_custom

urlpatterns = patterns('',
                       # django后台数据库管理
                       url(r'^admin/', include(admin.site.urls)),
                       # 用户账号--不要修改
                       url(r'^weixin/accounts/', include('account.urls')),
                       url(r'^accounts/', include('account.urls')),
                       # app系统控制（目前只包括功能控制开关，后续可扩展）--不要修改
                       url(r'^app_control/', include('app_control.urls')),
                       # 公告
                       url(r'notice/', include('notice.urls')),
                       )

# app自定义路径
urlpatterns += urlpatterns_custom

if settings.RUN_MODE == 'DEVELOP':
    urlpatterns += patterns('',
                            # media
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
                            )
