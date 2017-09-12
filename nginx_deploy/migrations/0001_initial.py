# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nginx_Group_Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(unique=True, max_length=80, verbose_name='\u4e1a\u52a1\u7ebf\u540d\u79f0')),
                ('comment', models.CharField(max_length=160, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nginx_Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='\u57df\u540d')),
                ('full_name', models.CharField(unique=True, max_length=80, verbose_name='\u914d\u7f6e\u6587\u4ef6\u540d\u79f0')),
                ('comment', models.CharField(max_length=160, null=True, blank=True)),
                ('group', models.ForeignKey(related_name='nginx_info', to='nginx_deploy.Nginx_Group_Info')),
            ],
        ),
        migrations.CreateModel(
            name='Nginx_Location_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_name', models.CharField(max_length=1000, null=True, verbose_name='locaton\u540d\u79f0', blank=True)),
                ('proxy_set_header', models.CharField(max_length=1000, null=True, verbose_name='\u8bf7\u6c42\u5934', blank=True)),
                ('proxy_pass', models.CharField(max_length=256, null=True, verbose_name='URL\u8f6c\u53d1', blank=True)),
                ('proxy_connect_timeout', models.CharField(max_length=32, null=True, verbose_name='\u8fde\u63a5\u8d85\u65f6\u65f6\u95f4', blank=True)),
                ('proxy_cache', models.CharField(max_length=1000, null=True, verbose_name='cache\u76f8\u5173', blank=True)),
                ('fastcgi', models.CharField(max_length=1000, null=True, verbose_name='fastcgi\u76f8\u5173', blank=True)),
                ('other_location', models.CharField(max_length=1000, null=True, verbose_name='location\u5176\u5b83\u914d\u7f6e\u9879', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nginx_Server_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listen_post', models.CharField(max_length=32, null=True, verbose_name='\u865a\u62df\u4e3b\u673a\u670d\u52a1\u7aef\u53e3', blank=True)),
                ('server_name', models.CharField(max_length=512, null=True, verbose_name='server\u540d\u79f0', blank=True)),
                ('gzip', models.CharField(max_length=32, null=True, verbose_name='\u538b\u7f29\u5f00\u542f', blank=True)),
                ('gzip_types', models.CharField(default=b'', max_length=512, null=True, verbose_name='\u538b\u7f29\u7c7b\u578b', blank=True)),
                ('access_log', models.CharField(max_length=512, null=True, verbose_name='\u8bbf\u95ee\u65e5\u5fd7', blank=True)),
                ('error_log', models.CharField(max_length=512, null=True, verbose_name='\u9519\u8bef\u65e5\u5fd7', blank=True)),
                ('other_server', models.CharField(max_length=1000, null=True, verbose_name='server\u5176\u5b83\u914d\u7f6e\u9879', blank=True)),
                ('nginx_info', models.ManyToManyField(related_name='nginx_server_detail', to='nginx_deploy.Nginx_Info')),
            ],
        ),
        migrations.CreateModel(
            name='Nginx_Server_SSL_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listen_post', models.CharField(max_length=32, null=True, verbose_name='\u865a\u62df\u4e3b\u673a\u670d\u52a1\u7aef\u53e3', blank=True)),
                ('server_name', models.CharField(max_length=512, null=True, verbose_name='server\u540d\u79f0', blank=True)),
                ('ssl', models.CharField(max_length=32, null=True, verbose_name='SSL\u5f00\u542f', blank=True)),
                ('ssl_certificate', models.CharField(max_length=512, null=True, verbose_name='\u8bc1\u4e66\u6587\u4ef6', blank=True)),
                ('ssl_certificate_key', models.CharField(max_length=512, null=True, verbose_name='\u79c1\u94a5\u6587\u4ef6')),
                ('ssl_session_timeout', models.CharField(max_length=32, null=True, verbose_name='\u52a0\u5bc6\u53c2\u6570\u6700\u957f\u671f\u9650', blank=True)),
                ('ssl_protocols', models.CharField(max_length=256, null=True, verbose_name='\u6307\u5b9a\u534f\u8bae\u7248\u672c', blank=True)),
                ('ssl_ciphers', models.CharField(max_length=512, null=True, verbose_name='\u52a0\u5bc6\u65b9\u5f0f', blank=True)),
                ('ssl_prefer_server_ciphers', models.CharField(default=b'', max_length=32, null=True, verbose_name='\u534f\u8bae\u4f18\u5148', blank=True)),
                ('other_ssl', models.CharField(max_length=1000, null=True, verbose_name='ssl\u5176\u5b83\u914d\u7f6e\u9879', blank=True)),
                ('access_log', models.CharField(max_length=512, null=True, verbose_name='\u8bbf\u95ee\u65e5\u5fd7', blank=True)),
                ('error_log', models.CharField(max_length=512, null=True, verbose_name='\u9519\u8bef\u65e5\u5fd7', blank=True)),
                ('nginx_info', models.ManyToManyField(related_name='nginx_server_ssl_detail', to='nginx_deploy.Nginx_Info')),
            ],
        ),
        migrations.CreateModel(
            name='Nginx_Upstream_Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upstream_name', models.CharField(max_length=128, null=True, verbose_name='upstream\u540d\u79f0', blank=True)),
                ('ip_port', models.CharField(max_length=256, null=True, verbose_name='IP+PORT', blank=True)),
                ('weight', models.CharField(default=b'', max_length=32, null=True, verbose_name='\u6743\u91cd', blank=True)),
                ('max_fails', models.CharField(max_length=32, null=True, verbose_name='\u8bf7\u6c42\u5931\u8d25\u6b21\u6570', blank=True)),
                ('fail_timeout', models.CharField(max_length=32, null=True, verbose_name='\u6682\u505c\u670d\u52a1\u65f6\u95f4', blank=True)),
                ('nginx_info', models.ForeignKey(related_name='nginx_upstream_detail', to='nginx_deploy.Nginx_Info')),
            ],
        ),
        migrations.AddField(
            model_name='nginx_location_detail',
            name='nginx_server',
            field=models.ManyToManyField(related_name='nginx_location_detail', to='nginx_deploy.Nginx_Server_Detail'),
        ),
        migrations.AddField(
            model_name='nginx_location_detail',
            name='nginx_server_ssl',
            field=models.ManyToManyField(related_name='nginx_location_detail', to='nginx_deploy.Nginx_Server_SSL_Detail'),
        ),
    ]
