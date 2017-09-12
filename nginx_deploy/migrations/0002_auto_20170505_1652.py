# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx_deploy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nginx_server_ssl_detail',
            name='server_name',
        ),
        migrations.AddField(
            model_name='nginx_server_ssl_detail',
            name='server_ssl_name',
            field=models.CharField(max_length=512, null=True, verbose_name='server_ssl\u540d\u79f0', blank=True),
        ),
    ]
