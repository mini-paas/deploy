# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx_deploy', '0003_auto_20170622_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginx_upstream_detail',
            name='ip_port',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='IP+PORT', blank=True),
        ),
    ]
