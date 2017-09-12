# coding:utf-8
from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=64, blank=True, db_index=True, null=True)

    def __unicode__(self):
        return self.username


class Hosts(models.Model):
    host_ip = models.CharField(max_length=128, blank=True, db_index=True, null=True)

    def __str__(self):
        return self.host_ip


class HostUsers(models.Model):
    host_user = models.CharField(max_length=64, blank=True, db_index=True, null=True)
    host_password = models.CharField(max_length=128, blank=True, db_index=True, null=True)
    host = models.ForeignKey('Hosts')

    def __str__(self):
        return '%s(%s)' % (self.host_user, self.host_password)


class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    task_type_choices = (("nginxdeploy", 'nginx_deploy'), ("initialize", 'initialization'))
    task_type = models.CharField(choices=task_type_choices, max_length=50)
    task_business = models.CharField(max_length=1024, blank=True, db_index=True, null=True)
    hosts = models.ManyToManyField('Hosts')
    user = models.ForeignKey('Users')
    task_content = models.TextField()
    task_pid = models.IntegerField(default=0)

    def __str__(self):
        return "taskid:%s task_content:%s" % (self.id, self.task_content)


class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey(TaskLog, related_name='tasklogdetail')
    host = models.ForeignKey('Hosts')
    date = models.DateTimeField(auto_now_add=True)
    event_log = models.TextField()
    result_choices = (('ok', 'Ok'), ('failed', 'Failed'), ('unknown', 'Unknown'))
    result = models.CharField(choices=result_choices, max_length=32, db_index=True, default='unknown')

    def __str__(self):
       return "child of:%s result:%s" % (self.child_of_task.id, self.result)


class FileList(models.Model):
    user = models.ForeignKey('Users')
    file_name = models.CharField(blank=True, null=True, max_length=128)
    file_size = models.CharField(blank=True, null=True, max_length=64)
    file_create_time = models.CharField(blank=True, null=True, max_length=64)
    files_dir = models.CharField(blank=True, null=True, max_length=64)

    def __unicode__(self):
        return self.file_name