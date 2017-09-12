# coding:utf-8

from rest_framework import generics
from serializers import *


class TaskLogViewListSet(generics.ListCreateAPIView):
    queryset = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
    serializer_class = TaskLogSerializer


class TaskLogViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
    serializer_class = TaskLogSerializer
