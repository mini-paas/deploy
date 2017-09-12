from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from base.views import *


urlpatterns = patterns('base.views',
    url(r'^$', index, name='index'),
    url(r'^recent/tasks/$', recent_tasks, name='recent_tasks'),
    url(r'^nginx/', include('nginx_deploy.urls')),
    url(r'^deploy/', include('deploy.urls')),
    url(r'^dashboard/data/$', dashboard_datas, name='dashboard_datas'),
)
