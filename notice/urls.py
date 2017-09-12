# -*- coding: utf-8 -*-

from django.conf.urls import patterns


urlpatterns = patterns('notice.views',
                       # 通知中心
                       (r'^$', 'notice_home'),
                       )
