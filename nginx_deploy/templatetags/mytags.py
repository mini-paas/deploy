# coding: utf-8

from django import template
from nginx_deploy.deploy_conf import *
from nginx_deploy.models import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

register = template.Library()


@register.filter(name='infor_full_name')
def infor_full_name(infor_id):
    infor = get_object(Nginx_Info, id=infor_id)
    if infor:
        return str(infor.group.groupname+'__'+infor.full_name)
    else:
        pass


@register.filter(name='server_infor_fullname')
def server_infor_fullname(server_id):
    server = get_object(Nginx_Server_Detail, id=server_id)
    if server.nginx_info.values('full_name'):
        infor_id = server.nginx_info.values('id')[0].get('id')
        infor = get_object(Nginx_Info, id=infor_id)
        groupname = infor.group.groupname
        fullname = server.nginx_info.values('full_name')[0].get('full_name')
        return str(groupname+'__'+fullname)
    else:
        return 0


@register.filter(name='server_ssl_infor_fullname')
def server_ssl_infor_fullname(server_ssl_id):
    server_ssl = get_object(Nginx_Server_SSL_Detail, id=server_ssl_id)
    if server_ssl.nginx_info.values('full_name'):
        infor_id = server_ssl.nginx_info.values('id')[0].get('id')
        infor = get_object(Nginx_Info, id=infor_id)
        groupname = infor.group.groupname
        fullname = server_ssl.nginx_info.values('full_name')[0].get('full_name')
        return str(groupname+'__'+fullname)
    else:
        return 0


@register.filter(name='location_server_name')
def location_server_name(location_id):
    location = get_object(Nginx_Location_Detail, id=location_id)
    if location.nginx_server.values('server_name'):
        return location.nginx_server.values('server_name')[0].get('server_name')
    else:
        return 0


@register.filter(name='location_server_ssl_name')
def location_server_ssl_name(location_id):
    location = get_object(Nginx_Location_Detail, id=location_id)
    if location.nginx_server_ssl.values('server_ssl_name'):
        return location.nginx_server_ssl.values('server_ssl_name')[0].get('server_ssl_name')
    else:
        return 0


@register.filter(name='detail_upstream_name')
def detail_upstream_name(infor_id):
    infor = get_object(Nginx_Info, id=infor_id)
    if infor.nginx_upstream_detail.values('upstream_name'):
        return infor.nginx_upstream_detail.values('upstream_name')[0].get('upstream_name')
    else:
        return 0


@register.filter(name='detail_location_proxy_set_header')
def detail_location_proxy_set_header(infor_id):
    infor = get_object(Nginx_Info, id=infor_id)
    if infor.nginx_server_detail.values('id'):
        a = infor.nginx_server_detail.values('id')[0].get('id')
        server = get_object(Nginx_Server_Detail, id=a)
        if server.nginx_location_detail.values('proxy_set_header'):
            return server.nginx_location_detail.values('proxy_set_header')[0].get('proxy_set_header')
        else:
            return 0
    else:
        return 0


@register.filter(name='detail_location_proxy_pass')
def detail_location_proxy_pass(infor_id):
    infor = get_object(Nginx_Info, id=infor_id)
    if infor.nginx_server_detail.values('id'):
        a = infor.nginx_server_detail.values('id')[0].get('id')
        server = get_object(Nginx_Server_Detail, id=a)
        if server.nginx_location_detail.values('proxy_pass'):
            return server.nginx_location_detail.values('proxy_pass')[0].get('proxy_pass')
        else:
            return 0
    else:
        return 0


@register.filter(name='detail_location_proxy_connect_timeout')
def detail_location_proxy_connect_timeout(infor_id):
    infor = get_object(Nginx_Info, id=infor_id)
    if infor.nginx_server_detail.values('id'):
        a = infor.nginx_server_detail.values('id')[0].get('id')
        server = get_object(Nginx_Server_Detail, id=a)
        if server.nginx_location_detail.values('proxy_connect_timeout'):
            return server.nginx_location_detail.values('proxy_connect_timeout')[0].get('proxy_connect_timeout')
        else:
            return 0
    else:
        return 0

