from django.conf.urls import url, patterns
from views import *


urlpatterns = patterns('deploy.views',
    url(r'task_list/conf$', task_list, name='task_list'),
    url(r'task/action/$', task_action, name='task_action'),
    url(r'task/res/$', task_res, name='task_res'),
    url(r'task/abort/$', task_abort, name='task_abort'),
    url(r'conf_list/$', conf_list, name='conf_list'),
    url(r'task/file_upload/$', task_file_upload, name='file_upload'),
    url(r'task/file_upload/(\w+)/delete/$', delete_file, name='delete_file'),
    url(r'task/file_download/(\w+)/$', file_download, name='file_download_url'),
    url(r'task/file/$', task_file, name='task_file'),
    #url(r'tasks/list/$', define_tasks, name='define_tasks'),
    url(r'tasks/list/$', define_tasks.as_view(), name='define_tasks'),
    url(r'task/list/$', define_task_list, name='define_task_list'),
)
