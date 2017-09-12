# -*- coding: utf-8 -*-

from django.db import models


class Nginx_Group_Info(models.Model):
    groupname = models.CharField(max_length=80, unique=True, verbose_name=u"业务线名称")
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.groupname


class Nginx_Info(models.Model):
    name = models.CharField(max_length=80, blank=True, unique=True, verbose_name=u"域名")
    full_name = models.CharField(max_length=80, unique=True, verbose_name=u"配置文件名称")
    comment = models.CharField(max_length=160, blank=True, null=True)
    group = models.ForeignKey(Nginx_Group_Info, related_name='nginx_info')

    def __unicode__(self):
        return self.full_name


class Nginx_Upstream_Detail(models.Model):
    upstream_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"upstream名称")
    ip_port = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"IP+PORT")
    weight = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"权重")
    max_fails = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"请求失败次数")
    fail_timeout = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"暂停服务时间")
    nginx_info = models.ForeignKey(Nginx_Info, related_name='nginx_upstream_detail')

    def __unicode__(self):
        return self.upstream_name


class Nginx_Server_Detail(models.Model):

    listen_post = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"虚拟主机服务端口")
    server_name = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"server名称")
    gzip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"压缩开启")
    gzip_types = models.CharField(max_length=512, blank=True, null=True, default='', verbose_name=u"压缩类型")
    access_log = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"访问日志")
    error_log = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"错误日志")
    other_server = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"server其它配置项")
    nginx_info = models.ManyToManyField(Nginx_Info, related_name='nginx_server_detail')

    def __unicode__(self):
        return self.server_name


class Nginx_Server_SSL_Detail(models.Model):

    listen_post = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"虚拟主机服务端口")
    server_ssl_name = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"server_ssl名称")
    ssl = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"SSL开启")
    ssl_certificate = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"证书文件")
    ssl_certificate_key = models.CharField(max_length=512, null=True, verbose_name=u'私钥文件')
    ssl_session_timeout = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"加密参数最长期限")
    ssl_protocols = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"指定协议版本")
    ssl_ciphers = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"加密方式")
    ssl_prefer_server_ciphers = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"协议优先")
    other_ssl = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"ssl其它配置项")
    access_log = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"访问日志")
    error_log = models.CharField(max_length=512, blank=True, null=True, verbose_name=u"错误日志")
    nginx_info = models.ManyToManyField(Nginx_Info, related_name='nginx_server_ssl_detail')

    def __unicode__(self):
        return self.server_ssl_name


class Nginx_Location_Detail(models.Model):

    location_name = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"locaton名称")
    proxy_set_header = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"请求头")
    proxy_pass = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"URL转发")
    proxy_connect_timeout = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"连接超时时间")
    proxy_cache = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"cache相关")
    fastcgi = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"fastcgi相关")
    other_location = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u"location其它配置项")
    nginx_server = models.ManyToManyField(Nginx_Server_Detail, related_name='nginx_location_detail')
    nginx_server_ssl = models.ManyToManyField(Nginx_Server_SSL_Detail, related_name='nginx_location_detail')

    def __unicode__(self):
        return self.location_name
