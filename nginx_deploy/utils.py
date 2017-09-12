from nginx_deploy.models import *


def nginxinfor_detail(nginx_infor_id):
    global servers, server_ssls

    infor_info = Nginx_Info.objects.get(id=nginx_infor_id)
    upstreams = list(infor_info.nginx_upstream_detail.values('ip_port', 'weight', 'max_fails', 'fail_timeout'))
    if infor_info.nginx_server_detail.values('listen_post'):
        servers = infor_info.nginx_server_detail.values('listen_post', 'server_name', 'gzip', 'access_log', 'error_log', 'gzip_types')[0]
    if infor_info.nginx_server_ssl_detail.values('listen_post'):
        server_ssls = infor_info.nginx_server_ssl_detail.values('listen_post', 'server_ssl_name', 'access_log', 'error_log', 'ssl', 'ssl_certificate', 'ssl_certificate_key', 'ssl_session_timeout', 'ssl_protocols', 'ssl_ciphers', 'ssl_prefer_server_ciphers', 'other_ssl')[0]
    server_id = infor_info.nginx_server_detail.values('id')
    server = Nginx_Server_Detail.objects.get(id=server_id)
    locations = server.nginx_location_detail.values('location_name', 'proxy_connect_timeout', 'proxy_pass', 'proxy_set_header','proxy_cache', 'fastcgi', 'other_location')[0]
    upstream = infor_info.nginx_upstream_detail.values('upstream_name')[0]

    return upstreams, upstream, servers, server_ssls, locations

