# from django.contrib import admin
#
# # Register your models here.
# from django.contrib import admin
# # import from apps here
# from deploy.models import Users
#
#
# admin.site.register(Users)
from django.contrib import admin
# import from apps here
from deploy.models import *

admin.site.register(TaskLogDetail)
admin.site.register(TaskLog)
