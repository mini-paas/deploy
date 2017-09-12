# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_auto_20170622_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=128, null=True, blank=True)),
                ('file_size', models.CharField(max_length=64, null=True, blank=True)),
                ('file_create_time', models.CharField(max_length=64, null=True, blank=True)),
                ('files_dir', models.CharField(max_length=64, null=True, blank=True)),
                ('user', models.ForeignKey(to='deploy.Users')),
            ],
        ),
    ]
