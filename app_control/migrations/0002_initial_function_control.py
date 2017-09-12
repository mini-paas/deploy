# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations
from app_control.models import Function_controller


def initial_function_control_data(apps, schema_editor):
    try:
        # 初始化功能开关数据
        Function_controller.objects.bulk_create([
            Function_controller(func_code='func_test', func_name=u"示例功能"),
            Function_controller(func_code='create_task', func_name=u"创建任务"),
            Function_controller(func_code='execute_task', func_name=u"执行任务"),
            Function_controller(func_code='tasks', func_name=u"任务列表"),
            Function_controller(func_code='task', func_name=u"任务详情"),
            Function_controller(func_code='pause_task', func_name=u"任务暂停"),
            Function_controller(func_code='terminate_task', func_name=u"任务终止"),
        ])
    except:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_function_control_data),
    ]
