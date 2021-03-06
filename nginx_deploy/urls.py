# coding=utf-8

from django.conf.urls import patterns, include, url
from nginx_deploy.views import *

urlpatterns = patterns('nginx_deploy.views',
    url(r'^group/add/$', group_add, name='group_add'),
    url(r'^group/list/$', group_list, name='group_list'),
    url(r'^group/edit/$', group_edit, name='group_edit'),
    url(r'^group/del/$', group_del, name='group_del'),
    url(r'^infor/add/$', infor_add, name='infor_add'),
    url(r'^infor/list/$', infor_list, name='infor_list'),
    url(r'^infor/edit/$', infor_edit, name='infor_edit'),
    url(r'^infor/detail/$', infor_detail, name='infor_detail'),
    url(r'^infor/del/$', infor_del, name='infor_del'),
    url(r'^upstream/add/$', upstream_add, name='upstream_add'),
    url(r'^upstream/grouplist/$', upstream_grouplist, name='upstream_grouplist'),
    url(r'^upstream/list/$', upstream_list, name='upstream_list'),
    url(r'^upstream/edit/$', upstream_edit, name='upstream_edit'),
    url(r'^upstream/del/$', upstream_del, name='upstream_del'),
    url(r'^server/add/$', server_add, name='server_add'),
    url(r'^server/list/$', server_list, name='server_list'),
    url(r'^server/edit/$', server_edit, name='server_edit'),
    url(r'^server/del/$', server_del, name='server_del'),
    url(r'^server/ssl/add/$', server_ssl_add, name='server_ssl_add'),
    url(r'^server/ssl/list/$', server_ssl_list, name='server_ssl_list'),
    url(r'^server/ssl/edit/$', server_ssl_edit, name='server_ssl_edit'),
    url(r'^server/ssl/del/$', server_ssl_del, name='server_ssl_del'),
    url(r'^location/add/$', location_add, name='location_add'),
    url(r'^location/list/$', location_list, name='location_list'),
    url(r'^location/edit/$', location_edit, name='location_edit'),
    url(r'^location/del/$', location_del, name='location_del'),
    url(r'^infor/list/nginxtest/detail/$', nginxtest_detail, name='nginxtest_detail'),
    url(r'^upstream/edit/get/$', upstream_edit_get, name='upstream_edit_get'),
)
