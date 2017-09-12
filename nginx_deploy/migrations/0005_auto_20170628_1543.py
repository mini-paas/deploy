# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx_deploy', '0004_auto_20170628_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginx_location_detail',
            name='proxy_pass',
            field=models.CharField(max_length=255, null=True, verbose_name='URL\u8f6c\u53d1', blank=True),
        ),
        migrations.AlterField(
            model_name='nginx_server_ssl_detail',
            name='ssl_protocols',
            field=models.CharField(max_length=255, null=True, verbose_name='\u6307\u5b9a\u534f\u8bae\u7248\u672c', blank=True),
        ),
        migrations.AlterField(
            model_name='nginx_upstream_detail',
            name='ip_port',
            field=models.CharField(max_length=255, null=True, verbose_name='IP+PORT', blank=True),
        ),
    ]
