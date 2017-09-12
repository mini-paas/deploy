# -*- coding: utf-8 -*-

from deploy_conf import *
from nginx_deploy.models import *
from deploy.utils import *
from utils import *
import json
import socket
import time
import rpyc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def group_add(request):
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        groupname = request.POST.get('group_name')
        comment = request.POST.get('comment')

        p = Nginx_Group_Info(groupname=groupname, comment=comment)
        p.save()
        return HttpResponseRedirect(reverse('group_list'))

    return my_render('nginx_deploy/group_add.html', locals(), request)


def group_edit(request):
    group_id = request.GET.get('id')
    group = Nginx_Group_Info.objects.get(id=group_id)

    if request.method == 'POST':
        groupname = request.POST.get('group_name')
        comment = request.POST.get('comment')

        Nginx_Group_Info.objects.filter(id=group_id).update(groupname=groupname, comment=comment)
        return HttpResponseRedirect(reverse('group_list'))

    return my_render('nginx_deploy/group_edit.html', locals(), request)


def group_list(request):
    group_all = Nginx_Group_Info.objects.all()
    group_id = request.GET.get('id')
    if group_id:
        group_all = Nginx_Group_Info.objects.filter(id=group_id)
    group_info_list, p, groups, page_range, current_page, show_first, show_end = pages(group_all, request)

    return my_render('nginx_deploy/group_list.html', locals(), request)


def group_del(request):

    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Group_Info.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def infor_edit(request):
    infor_id = request.GET.get('id')
    infor = Nginx_Info.objects.get(id=infor_id)
    group_all = Nginx_Group_Info.objects.all()

    if request.method == 'POST':
        name = request.POST.get('domain_name')
        full_name = request.POST.get('infor_name')
        groups_selected = request.POST.get('infors')
        group = Nginx_Group_Info.objects.get(id=groups_selected)
        comment = request.POST.get('comment')

        Nginx_Info.objects.filter(id=infor_id).update(name=name, full_name=full_name, group=group, comment=comment)
        return HttpResponseRedirect(reverse('infor_list'))

    return my_render('nginx_deploy/infor_edit.html', locals(), request)


def infor_add(request):
    group_all = Nginx_Group_Info.objects.all()

    if request.method == 'POST':
        name = request.POST.get('domain_name')
        full_name = request.POST.get('infor_name')
        groups_selected = request.POST.get('infors')
        group = Nginx_Group_Info.objects.get(id=groups_selected)
        comment = request.POST.get('comment')

        p = Nginx_Info(name=name, full_name=full_name, group=group, comment=comment)
        p.save()
        return HttpResponseRedirect(reverse('infor_list'))

    return my_render('nginx_deploy/infor_add.html', locals(), request)


def infor_detail(request):
    infor_id = request.GET.get('id')
    infor_info = Nginx_Info.objects.get(id=infor_id)
    upstreams = infor_info.nginx_upstream_detail.values('ip_port', 'upstream_name', 'weight', 'max_fails', 'fail_timeout')
    if infor_info.nginx_server_detail.values('listen_post'):
        servers = infor_info.nginx_server_detail.values('other_server', 'listen_post', 'server_name', 'gzip', 'access_log', 'error_log', 'gzip_types')[0]
    if infor_info.nginx_server_ssl_detail.values('listen_post'):
        server_ssls = infor_info.nginx_server_ssl_detail.values('listen_post', 'server_ssl_name', 'access_log', 'error_log', 'ssl', 'ssl_certificate', 'ssl_certificate_key', 'ssl_session_timeout', 'ssl_protocols', 'ssl_ciphers', 'ssl_prefer_server_ciphers', 'other_ssl')[0]
    if infor_info.nginx_server_detail.values('id'):
        a = infor_info.nginx_server_detail.values('id')[0].get('id')
        server = get_object(Nginx_Server_Detail, id=a)
        locations = server.nginx_location_detail.values('location_name', 'proxy_set_header', 'proxy_pass', 'proxy_connect_timeout', 'proxy_cache', 'fastcgi', 'other_location')
    if infor_info.nginx_server_ssl_detail.values('id'):
        a = infor_info.nginx_server_ssl_detail.values('id')[0].get('id')
        server_ssl = get_object(Nginx_Server_SSL_Detail, id=a)
        locations_ssl = server_ssl.nginx_location_detail.values('location_name', 'proxy_set_header', 'proxy_pass', 'proxy_connect_timeout', 'proxy_cache', 'fastcgi', 'other_location')

    return my_render('nginx_deploy/infor_detail.html', locals(), request)


def infor_list(request):
    group_id = request.GET.get('group_id')
    infor_id = request.GET.get('infor_id')
    server_id = request.GET.get('server_id')
    server_ssl_id = request.GET.get('server_ssl_id')
    infor_all = Nginx_Info.objects.all()
    if group_id:
        infor_all = Nginx_Info.objects.filter(group_id=group_id)
    if infor_id:
        infor_all = Nginx_Info.objects.filter(id=infor_id)
    if server_id:
        server_info = Nginx_Server_Detail.objects.get(id=server_id)
        infor_all = server_info.nginx_info.all()
    if server_ssl_id:
        server_ssl_info = Nginx_Server_SSL_Detail.objects.get(id=server_ssl_id)
        infor_all = server_ssl_info.nginx_info.all()
    infor_list, p, infors, page_range, current_page, show_first, show_end = pages(infor_all, request)

    return my_render('nginx_deploy/infor_list.html', locals(), request)


def infor_del(request):
    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Info.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def upstream_add(request):

    if request.method == 'POST':

        upstreams = request.POST.get('upstreams')
        upstreams = json.loads(upstreams)
        for i in upstreams:
            upstream = i.get('upstream')
            ip_port = i.get('ip_port')
            weight = i.get('weight')
            max_fails = i.get('max_fails')
            fail_timeout = i.get('fail_timeout')
            group_selected = i.get('groups')
            infors_selected = i.get('infors')
            nginx_info = Nginx_Info.objects.get(full_name=infors_selected)
            p = Nginx_Upstream_Detail(upstream_name=upstream, ip_port=ip_port, weight=weight, max_fails=max_fails, fail_timeout=fail_timeout, nginx_info=nginx_info)
            p.save()

        return HttpResponse('UpstreamAddSuccess')

    return my_render('nginx_deploy/upstream_add.html', locals(), request)


def upstream_edit(request):
    upstream_id = request.GET.get('id')
    upstream = Nginx_Upstream_Detail.objects.get(id=upstream_id)
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        upstream = request.POST.get('upstreams')
        upstreams = json.loads(upstream)
        upstream = upstreams.get('upstream')
        ip_port = upstreams.get('ip_port')
        weight = upstreams.get('weight')
        max_fails = upstreams.get('max_fails')
        fail_timeout = upstreams.get('fail_timeout')
        infors_selected = upstreams.get('infors')
        nginx_info = Nginx_Info.objects.get(full_name=infors_selected)
        Nginx_Upstream_Detail.objects.filter(id=upstream_id).update(upstream_name=upstream, ip_port=ip_port, weight=weight, max_fails=max_fails, fail_timeout=fail_timeout, nginx_info=nginx_info)
        return HttpResponseRedirect(reverse('upstream_list'))

    return my_render('nginx_deploy/upstream_edit.html', locals(), request)


def upstream_edit_get(request):
    upstream_id = request.GET.get('id')
    upstream = Nginx_Upstream_Detail.objects.get(id=upstream_id)
    upstreams = {'id': upstream.id, 'upstream_name': upstream.upstream_name, 'ip_port': upstream.ip_port, 'weight': upstream.weight, 'max_fails': upstream.max_fails, 'fail_timeout': upstream.fail_timeout, 'groups': upstream.nginx_info.group.groupname, 'infors': upstream.nginx_info.full_name}
    upstream_result = json.dumps(upstreams)

    return HttpResponse(upstream_result)


def upstream_list(request):
    infor_id = request.GET.get('infor_id')
    upstream_id = request.GET.get('id')
    upstream_all = Nginx_Upstream_Detail.objects.all()
    if infor_id:
        upstream_all = Nginx_Upstream_Detail.objects.filter(nginx_info_id=infor_id)
    if upstream_id:
        upstreamname = Nginx_Upstream_Detail.objects.get(id=upstream_id)
        upstream_all = Nginx_Upstream_Detail.objects.filter(upstream_name=upstreamname.upstream_name)
    upstream_list, p, upstreams, page_range, current_page, show_first, show_end = pages(upstream_all, request)

    return my_render('nginx_deploy/upstream_list.html', locals(), request)


def upstream_grouplist(request):
    upstream_all = Nginx_Upstream_Detail.objects.values('upstream_name').distinct()
    upstreamss = Nginx_Upstream_Detail.objects.all()
    upstream_list, p, upstreams, page_range, current_page, show_first, show_end = pages(upstream_all, request)

    return my_render('nginx_deploy/upstream_grouplist.html', locals(), request)


def upstream_del(request):

    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Upstream_Detail.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def server_add(request):
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        server = request.POST.get('server')
        servers = json.loads(server)
        listen = servers.get('listen')
        server_name = servers.get('server_name')
        gzip = servers.get('optionsRadios')
        gzip_types = servers.get('gzip_types')
        access_log = servers.get('access_log')
        if '&nbsp;' in access_log:
            access_log = access_log.replace('&nbsp;', ' ')
        error_log = servers.get('error_log')
        other_server = servers.get('server_other')
        if '&nbsp;' in other_server:
            other_server = other_server.replace('&nbsp;', ' ')
        infors = servers.get('infors')
        infors_selected = Nginx_Info.objects.get(full_name=infors)
        infors_selected = infors_selected.id

        p = Nginx_Server_Detail(listen_post=listen, server_name=server_name, gzip=gzip, gzip_types=gzip_types, access_log=access_log, error_log=error_log, other_server=other_server)
        p.save()
        p = Nginx_Server_Detail.objects.get(server_name=server_name)

        if infors_selected:
            p.nginx_info.add(infors_selected)
            p.save()
        else:
            pass

    return my_render('nginx_deploy/server_add.html', locals(), request)


def server_edit(request):
    server_id = request.GET.get('id')
    servers = Nginx_Server_Detail.objects.get(id=server_id)
    if servers.nginx_info.values('full_name'):
        infor_id = servers.nginx_info.values('id')[0].get('id')
        infor = get_object(Nginx_Info, id=infor_id)
        groupname = infor.group.groupname
        fullname = servers.nginx_info.values('full_name')[0].get('full_name')
    else:
        groupname, fullname = '', ''
    server = {'id': servers.id, 'gzip': servers.gzip, 'listen_post': servers.listen_post, 'server_name': servers.server_name, 'gzip_types': servers.gzip_types, 'access_log': servers.access_log, 'error_log': servers.error_log, 'other_server': servers.other_server, 'groups': groupname, 'infors': fullname}
    gzip_role = {'on': 'on', 'off': 'off'}
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        server = request.POST.get('server')
        servers = json.loads(server)
        listen = servers.get('listen')
        server_name = servers.get('server_name')
        gzip = servers.get('gzip')
        gzip_types = servers.get('gzip_types')
        access_log = servers.get('access_log')
        if '&nbsp;' in access_log:
            access_log = access_log.replace('&nbsp;', ' ')
        error_log = servers.get('error_log')
        other_server = servers.get('server_other')
        if '&nbsp;' in other_server:
            other_server = other_server.replace('&nbsp;', ' ')
        infors = servers.get('infors')
        infors_selected = Nginx_Info.objects.get(full_name=infors)
        infors_selected = infors_selected.id

        Nginx_Server_Detail.objects.filter(id=server_id).update(listen_post=listen, server_name=server_name, gzip=gzip, gzip_types=gzip_types, access_log=access_log, error_log=error_log, other_server=other_server)
        p = Nginx_Server_Detail.objects.get(id=server_id)
        p.nginx_info.clear()

        if infors_selected:
            p.nginx_info.add(infors_selected)
        else:
            pass

    return my_render('nginx_deploy/server_edit.html', locals(), request)


def server_list(request):
    infor_id = request.GET.get('infor_id')
    location_id = request.GET.get('location_id')
    server_all = Nginx_Server_Detail.objects.all()
    if infor_id:
        nginx_info = Nginx_Info.objects.get(id=infor_id)
        server_all = nginx_info.nginx_server_detail.all()
    if location_id:
        location_info = Nginx_Location_Detail.objects.get(id=location_id)
        server_all = location_info.nginx_server.all()
    server_list, p, servers, page_range, current_page, show_first, show_end = pages(server_all, request)

    return my_render('nginx_deploy/server_list.html', locals(), request)


def server_del(request):

    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Server_Detail.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def server_ssl_add(request):
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        server_ssl = request.POST.get('server_ssl')
        server_ssls = json.loads(server_ssl)
        listen = server_ssls.get('listen')
        server_name = server_ssls.get('server_name')
        access_log = server_ssls.get('access_log')
        if '&nbsp;' in access_log:
            access_log = access_log.replace('&nbsp;', ' ')
        error_log = server_ssls.get('error_log')
        ssl = server_ssls.get('ssl')
        ssl_certificate = server_ssls.get('ssl_certificate')
        ssl_certificate_key = server_ssls.get('ssl_certificate_key')
        ssl_session_timeout = server_ssls.get('ssl_session_timeout')
        ssl_protocols = server_ssls.get('ssl_protocols')
        if '&nbsp;' in ssl_protocols:
            ssl_protocols = ssl_protocols.replace('&nbsp;', ' ')
        ssl_ciphers = server_ssls.get('ssl_ciphers')
        ssl_prefer_server_ciphers = server_ssls.get('ssl_prefer_server_ciphers')
        other_ssl = server_ssls.get('ssl_other')
        infors = server_ssls.get('infors')
        infors_selected = Nginx_Info.objects.get(full_name=infors)
        infors_selected = infors_selected.id

        p = Nginx_Server_SSL_Detail(listen_post=listen, server_ssl_name=server_name, access_log=access_log, error_log=error_log, ssl=ssl, ssl_certificate=ssl_certificate, ssl_certificate_key=ssl_certificate_key, ssl_session_timeout=ssl_session_timeout, ssl_protocols=ssl_protocols, ssl_ciphers=ssl_ciphers, ssl_prefer_server_ciphers=ssl_prefer_server_ciphers, other_ssl=other_ssl)
        p.save()

        p = Nginx_Server_SSL_Detail.objects.get(server_ssl_name=server_name)

        if infors_selected:
            p.nginx_info.add(infors_selected)
            p.save()
        else:
            pass

    return my_render('nginx_deploy/server_ssl_add.html', locals(), request)


def server_ssl_edit(request):
    server_ssl_id = request.GET.get('id')
    server_ssl = Nginx_Server_SSL_Detail.objects.get(id=server_ssl_id)
    if server_ssl.nginx_info.values('full_name'):
        infor_id = server_ssl.nginx_info.values('id')[0].get('id')
        infor = get_object(Nginx_Info, id=infor_id)
        groupname = infor.group.groupname
        fullname = server_ssl.nginx_info.values('full_name')[0].get('full_name')
    else:
        groupname, fullname = '', ''
    server_ssl = {'id': server_ssl.id, 'listen_post': server_ssl.listen_post, 'ssl': server_ssl.ssl, 'server_ssl_name':server_ssl.server_ssl_name, 'ssl_certificate': server_ssl.ssl_certificate, 'ssl_certificate_key': server_ssl.ssl_certificate_key, 'ssl_session_timeout': server_ssl.ssl_session_timeout, 'ssl_protocols': server_ssl.ssl_protocols, 'ssl_ciphers': server_ssl.ssl_ciphers, 'ssl_prefer_server_ciphers': server_ssl.ssl_prefer_server_ciphers, 'other_ssl': server_ssl.other_ssl, 'access_log': server_ssl.access_log, 'error_log': server_ssl.error_log, 'groups': groupname, 'infors': fullname}
    ssl_role = {'on': 'on', 'off': 'off'}
    ssl_prefer_server_ciphers_role = {'on': 'on', 'off': 'off'}
    infor_all = Nginx_Info.objects.all()

    if request.method == 'POST':
        server_ssl = request.POST.get('server_ssl')
        server_ssls = json.loads(server_ssl)
        listen = server_ssls.get('listen')
        server_ssl_name = server_ssls.get('server_ssl_name')
        access_log = server_ssls.get('access_log')
        if '&nbsp;' in access_log:
            access_log = access_log.replace('&nbsp;', ' ')
        error_log = server_ssls.get('error_log')
        ssl = server_ssls.get('ssl')
        ssl_certificate = server_ssls.get('ssl_certificate')
        ssl_certificate_key = server_ssls.get('ssl_certificate_key')
        ssl_session_timeout = server_ssls.get('ssl_session_timeout')
        ssl_protocols = server_ssls.get('ssl_protocols')
        if '&nbsp;' in ssl_protocols:
            ssl_protocols = ssl_protocols.replace('&nbsp;', ' ')
        ssl_ciphers = server_ssls.get('ssl_ciphers')
        ssl_prefer_server_ciphers = server_ssls.get('ssl_prefer_server_ciphers')
        other_ssl = server_ssls.get('ssl_other')
        infors = server_ssls.get('infors')
        infors_selected = Nginx_Info.objects.get(full_name=infors)
        infors_selected = infors_selected.id

        Nginx_Server_SSL_Detail.objects.filter(id=server_ssl_id).update(listen_post=listen, server_ssl_name=server_ssl_name, access_log=access_log, error_log=error_log, ssl=ssl, ssl_certificate=ssl_certificate, ssl_certificate_key=ssl_certificate_key, ssl_session_timeout=ssl_session_timeout, ssl_protocols=ssl_protocols, ssl_ciphers=ssl_ciphers, ssl_prefer_server_ciphers=ssl_prefer_server_ciphers, other_ssl=other_ssl)
        p = Nginx_Server_SSL_Detail.objects.get(id=server_ssl_id)
        p.nginx_info.clear()

        if infors_selected:
            p.nginx_info.add(infors_selected)
        else:
            pass

    return my_render('nginx_deploy/server_ssl_edit.html', locals(), request)


def server_ssl_list(request):
    infor_id = request.GET.get('infor_id')
    location_id = request.GET.get('location_id')
    server_ssl_all = Nginx_Server_SSL_Detail.objects.all()
    if infor_id:
        nginx_info = Nginx_Info.objects.get(id=infor_id)
        server_ssl_all = nginx_info.nginx_server_ssl_detail.all()
    if location_id:
        location_info = Nginx_Location_Detail.objects.get(id=location_id)
        server_ssl_all = location_info.nginx_server_ssl.all()

    server_ssl_list, p, server_ssl_s, page_range, current_page, show_first, show_end = pages(server_ssl_all, request)

    return my_render('nginx_deploy/server_ssl_list.html', locals(), request)


def server_ssl_del(request):

    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Server_SSL_Detail.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def location_add(request):
    server_all = Nginx_Server_Detail.objects.all()
    server_ssl_all = Nginx_Server_SSL_Detail.objects.all()

    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        if '&nbsp;' in location_name:
            location_name = location_name.replace('&nbsp;', ' ')
        proxy_set_header = request.POST.get('proxy_set_header')
        if '&nbsp;' in proxy_set_header:
            proxy_set_header = proxy_set_header.replace('&nbsp;', ' ')
        proxy_pass = request.POST.get('proxy_pass')
        proxy_connect_timeout = request.POST.get('proxy_connect_timeout')
        proxy_cache = request.POST.get('proxy_cache')
        if '&nbsp;' in proxy_cache:
            proxy_cache = proxy_cache.replace('&nbsp;', ' ')
        fastcgi = request.POST.get('fastcgi')
        if '&nbsp;' in fastcgi:
            fastcgi = fastcgi.replace('&nbsp;', ' ')
        other_location = request.POST.get('other_location')
        if '&nbsp;' in other_location:
            other_location = other_location.replace('&nbsp;', ' ')
        servers_selected = request.POST.getlist('servers', '')
        servers_ssl_selected = request.POST.getlist('server_ssl_s', '')

        p = Nginx_Location_Detail(location_name=location_name, proxy_set_header=proxy_set_header, proxy_pass=proxy_pass, proxy_connect_timeout=proxy_connect_timeout, proxy_cache=proxy_cache, fastcgi=fastcgi, other_location=other_location)
        p.save()

        p = Nginx_Location_Detail.objects.get(proxy_pass=proxy_pass)

        if len(servers_selected) == 1:
            p.nginx_server.add(servers_selected[0])
            p.save()
        elif len(servers_selected) == 0:
            pass
        else:
            for server in servers_selected:
                p.nginx_server.add(server)
            p.save()

        if len(servers_ssl_selected) == 1:
            p.nginx_server_ssl.add(servers_ssl_selected[0])
            p.save()
        elif len(servers_ssl_selected) == 0:
            pass
        else:
            for servers_ssl in servers_ssl_selected:
                p.nginx_server_ssl.add(servers_ssl)
            p.save()

        return HttpResponseRedirect(reverse('location_list'))

    return my_render('nginx_deploy/location_add.html', locals(), request)


def location_edit(request):
    location_id = request.GET.get('id')
    location = Nginx_Location_Detail.objects.get(id=location_id)
    server_all = Nginx_Server_Detail.objects.all()
    server_ssl_all = Nginx_Server_SSL_Detail.objects.all()

    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        if '&nbsp;' in location_name:
            location_name = location_name.replace('&nbsp;', ' ')
        proxy_set_header = request.POST.get('proxy_set_header')
        if '&nbsp;' in proxy_set_header:
            proxy_set_header = proxy_set_header.replace('&nbsp;', ' ')
        proxy_pass = request.POST.get('proxy_pass')
        proxy_connect_timeout = request.POST.get('proxy_connect_timeout')
        proxy_cache = request.POST.get('proxy_cache')
        fastcgi = request.POST.get('fastcgi')
        other_location = request.POST.get('other_location')
        if '&nbsp;' in other_location:
            other_location = other_location.replace('&nbsp;', ' ')
        if '&nbsp;' in fastcgi:
            fastcgi = fastcgi.replace('&nbsp;', ' ')
        if '&nbsp;' in proxy_cache:
            proxy_cache = proxy_cache.replace('&nbsp;', ' ')
        servers_selected = request.POST.getlist('servers', '')
        servers_ssl_selected = request.POST.getlist('server_ssl_s', '')

        Nginx_Location_Detail.objects.filter(id=location_id).update(location_name=location_name, proxy_set_header=proxy_set_header, proxy_pass=proxy_pass, proxy_connect_timeout=proxy_connect_timeout, proxy_cache=proxy_cache, fastcgi=fastcgi, other_location=other_location)
        p = Nginx_Location_Detail.objects.get(id=location_id)
        p.nginx_server.clear()
        p.nginx_server_ssl.clear()

        if len(servers_selected) == 1:
            p.nginx_server.add(servers_selected[0])
        elif len(servers_selected) == 0:
            pass
        else:
            for server in servers_selected:
                p.nginx_server.add(server)

        if len(servers_ssl_selected) == 1:
            p.nginx_server_ssl.add(servers_ssl_selected[0])
        elif len(servers_ssl_selected) == 0:
            pass
        else:
            for servers_ssl in servers_ssl_selected:
                p.nginx_server_ssl.add(servers_ssl)

        return HttpResponseRedirect(reverse('location_list'))

    return my_render('nginx_deploy/location_edit.html', locals(), request)


def location_list(request):
    server_id = request.GET.get('server_id')
    server_ssl_id = request.GET.get('server_ssl_id')
    if server_id:
        server_info = Nginx_Server_Detail.objects.get(id=server_id)
        location_all = server_info.nginx_location_detail.all()
    if server_ssl_id:
        server_ssl_info = Nginx_Server_SSL_Detail.objects.get(id=server_ssl_id)
        location_all = server_ssl_info.nginx_location_detail.all()
    location_all = Nginx_Location_Detail.objects.all()
    location_list, p, locations, page_range, current_page, show_first, show_end = pages(location_all, request)

    return my_render('nginx_deploy/location_list.html', locals(), request)


def location_del(request):
    host_ids = request.GET.get('id')
    host_id_list = host_ids.split(',')
    for host_id in host_id_list:
        Nginx_Location_Detail.objects.filter(id=host_id).delete()

    return HttpResponse(u"del success!")


def nginxtest_detail(request):
    nginx_infor_id = request.GET.get('id')
    upstreams, upstream, servers, server_ssls, locations = nginxinfor_detail(nginx_infor_id)
    host_ids = ['10.247.135.236']
    push_resource = gen_resource(host_ids, user='mqq', passwdold='mqq2005')
    send = {'yml': u'nginx/nginx_test_qidian.yml', 'resource': push_resource, 'upstreams': upstreams, 'upstream': upstream, 'servers': servers, 'server_ssls': server_ssls, 'locations': locations}
    senddata = str(send)
    conn = rpyc.connect('10.173.25.36', 28080)
    conn.root.login('ANuser', 'KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    res = conn.root.Runcommands(senddata)

    return HttpResponse(json.dumps(res))
