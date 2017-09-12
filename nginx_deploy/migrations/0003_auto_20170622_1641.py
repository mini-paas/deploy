# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx_deploy', '0002_auto_20170505_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginx_info',
            name='name',
            field=models.CharField(unique=True, max_length=80, verbose_name='\u57df\u540d', blank=True),
        ),
    ]
