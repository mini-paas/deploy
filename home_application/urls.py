# -*- coding: utf-8 -*-

# import from apps here

# import from lib
from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
                       # 首页--your index
                       (r'^$', 'home'),
                       (r'^dev_guide/$', 'dev_guide'),
                       (r'^contact/$', 'contact'),
                       )
