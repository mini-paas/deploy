# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_ip', models.CharField(max_length=128, null=True, blank=True)),
                ('host_user', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('task_type', models.CharField(max_length=50, choices=[(b'nginxdeploy', b'nginx_deploy'), (b'initialize', b'initialization')])),
                ('task_business', models.CharField(max_length=128, null=True, blank=True)),
                ('task_content', models.TextField()),
                ('task_pid', models.IntegerField(default=0)),
                ('hosts', models.ManyToManyField(to='deploy.Hosts')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(default=b'unknown', max_length=32, choices=[(b'ok', b'Ok'), (b'failed', b'Failed'), (b'unknown', b'Unknown')])),
                ('child_of_task', models.ForeignKey(related_name='tasklogdetail', to='deploy.TaskLog')),
                ('host', models.ForeignKey(to='deploy.Hosts')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='tasklog',
            name='user',
            field=models.ForeignKey(to='deploy.Users'),
        ),
    ]
