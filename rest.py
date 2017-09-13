    url(r'tasks/list/$', define_tasks, name='define_tasks'),
    url(r'task/list/$', define_task_list, name='define_task_list'),

    tasks = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')

    tasks = TaskLog.objects.filter(user=user_name).filter(task_type='自定义任务').order_by('-id')


Router
get — list
post — create
get — retrieve
put — update
patch — partial-update
delete — destroy


ModelViewSet
list
create
retrieve
update
partial_update
destroy

from rest_framework import serializers
from deploy.models import *


class TaskLogSerializer(serializers.ModelSerializer):
    #hosts_amount = serializers.SerializerMethodField()
    #tasklogdetails = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskLogDetail.objects.all())

    class Meta:
        model = TaskLog
        fields = ('id', 'hosts', 'task_type', 'task_business', 'task_content', 'user')


# coding:utf-8

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView, Response
from serializers import *


# class TaskLogViewSet(viewsets.ModelViewSet):
#     queryset = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
#     serializer_class = TaskLogSerializer
#     permission_classes = (permissions.AllowAny,)
#     #permission_classes = (permissions.IsAuthenticated,)
#
#     def list(self, request, *args, **kwargs):
#         self.serializer_class = TaskLogSerializer
#         # queryset = self.queryset.prefetch_related('project__project')
#         # queryset = self.filter_queryset(queryset)
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     # def get(self, pk):
#     #     machine = self.get_object(pk)
#     #     serializer = TaskLogSerializer(machine)
#     #     return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         self.serializer_class = TaskLogSerializer
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         addlog.delay(request.user.username, 'Machine', '', 'asset_api.viewsets', '新增', request.data)
#         self.perform_create(serializer)
#         # logger.info('user: %s, create:(Machine)new, set:%s ', request.user.username, request.data)
#         return Response(serializer.data)
#
#     def update(self, request, *args, **kwargs):
#         self.serializer_class = TaskLogSerializer
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         addlog.delay(request.user.username, 'Machine', instance.id, 'asset_api.viewsets', '修改', instance.__dict__,
#                      request.data)
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#
#
#         return Response(serializer.data)

class TaskLogViewListSet(generics.ListCreateAPIView):
    queryset = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
    serializer_class = TaskLogSerializer


class TaskLogViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
    serializer_class = TaskLogSerializer


from django.conf.urls import url, include
from viewset import *
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.DefaultRouter()
# router.register(r'tasklog', TaskLogViewSet)
#
# urlpatterns = [
#         url(r'^', include(router.urls)),
#         url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
    url(r'^tasklog/$', TaskLogViewListSet.as_view()),
    url(r'^tasklog/(?P<pk>[0-9]+)/$', TaskLogViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)


