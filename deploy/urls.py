# coding=utf-8

from django.conf.urls import patterns, include, url
from deploy import api_urls, rest_urls
from deploy.views import *


urlpatterns = patterns('deploy.views',
    url(r'^hosts/multi/$', hosts_multi, name='hosts_multi'),
    url(r'^hosts/multi/filetrans/$', hosts_multi_filetrans, name="hosts_multi_filetrans"),
    url(r'^api/', include(api_urls)),
    #url(r'^rest/', include(rest_urls)),
    url(r'^user_audit/(\d+)/$', user_audit, name='user_audit'),
    url(r'^tasklog/detail/$', task_log_detail, name='task_log_detail'),
)
