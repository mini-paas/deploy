# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20170613_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosts',
            name='host_ip',
            field=models.CharField(db_index=True, max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hostusers',
            name='host_password',
            field=models.CharField(db_index=True, max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hostusers',
            name='host_user',
            field=models.CharField(db_index=True, max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tasklog',
            name='task_business',
            field=models.CharField(db_index=True, max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tasklogdetail',
            name='result',
            field=models.CharField(default=b'unknown', max_length=32, db_index=True, choices=[(b'ok', b'Ok'), (b'failed', b'Failed'), (b'unknown', b'Unknown')]),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(db_index=True, max_length=64, null=True, blank=True),
        ),
    ]
