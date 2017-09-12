from rest_framework import serializers
from deploy.models import *


class TaskLogSerializer(serializers.ModelSerializer):
    #tasklogdetails = serializers.PrimaryKeyRelatedField(many=True, queryset=TaskLogDetail.objects.all())


    class Meta:
        model = TaskLog
        fields = ('id', 'hosts', 'task_type', 'task_business', 'task_content', 'user')


