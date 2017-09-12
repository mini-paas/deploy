# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_user', models.CharField(max_length=64, null=True, blank=True)),
                ('host_password', models.CharField(max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hosts',
            name='host_user',
        ),
        migrations.AddField(
            model_name='hostusers',
            name='host',
            field=models.ForeignKey(to='deploy.Hosts'),
        ),
    ]
