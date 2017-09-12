# -*- coding: utf-8 -*-
from django.contrib import admin

from app_control.models import Function_controller


class Function_controllerAdmin(admin.ModelAdmin):
    list_display = ('func_code', 'func_name', 'enabled', 'create_time', 'func_developer')
    list_filter = ('func_code',)
    search_fields = ('func_code',)

admin.site.register(Function_controller, Function_controllerAdmin)
