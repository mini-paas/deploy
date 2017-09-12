# coding:utf-8
from deploy.views import *
from deploy.models import *
import datetime
import json


def index(request):
    return my_render('index.html', locals(), request)


def getDaysByNum():
    today = datetime.datetime.today()
    oldday = datetime.datetime(2017, 6, 1)
    num = (today - oldday).days
    oneday = datetime.timedelta(days=1)
    date_li, date_str = [], []
    for i in range(0, num):
        today = today-oneday
        date_li.append(today)
        date_str.append(str(today)[5:10])
    date_li.reverse()
    date_str.reverse()
    return date_li


def recent_tasks(request):
    task_log = []
    tasks = TaskLog.objects.filter(task_pid=0).order_by('-id')
    for task in tasks:
        tasks_dict = {'id': task.id, 'date': task.start_time, 'user': task.user.username, 'task_type': task.task_type, 'hosts': task.hosts.select_related().count(), 'business': task.task_business, 'finished_num': task.tasklogdetail.filter(result='ok').count(), 'failed_num': task.tasklogdetail.filter(result='failed').count(), 'unknown_num': task.tasklogdetail.filter(result='unknown').count(), 'content': task.task_content}
        task_log.append(tasks_dict)
    recent_tasks_list = json.dumps(task_log, default=json_date_handler)

    return HttpResponse(recent_tasks_list)


def dashboard_datas(request):
    index_data, detail_num, ips, user_top = [], [], [], {}
    start_time = datetime.date.today()
    end_time = start_time + datetime.timedelta(days=-7)
    STARTDATE = start_time.strftime("%Y-%m-%d 23:59:59")
    ENDDATE = end_time.strftime("%Y-%m-%d 00:00:00")
    users_num = {'users_num': Users.objects.count(), }
    ips_num = {'ips_num': Hosts.objects.count(), }
    ips.append(ips_num)
    ips_all = Hosts.objects.all()
    for i in ips_all:
        ips_dict = {'ip': i.host_ip, 'user': [a.host_user for a in i.hostusers_set.all()]}
        ips.append(ips_dict)
    task_type_num = {'命令执行': TaskLog.objects.filter(task_type=u'自定义任务').count(), 'nginx配置发布': TaskLog.objects.filter(task_type=u'nginx配置发布').count(), 'root密码修改': TaskLog.objects.filter(task_type=u'root密码修改').count(), '初始化': TaskLog.objects.filter(task_content=u'初始化').count(), 'site': TaskLog.objects.filter(task_content='site').count(), 'tomcat': TaskLog.objects.filter(task_content='tomcat').count(), }
    a = TaskLog.objects.filter(start_time__gte=ENDDATE, start_time__lte=STARTDATE)
    users_list = a.values('user').distinct()
    for i in users_list:
        user_top[Users.objects.filter(id=i.get('user')).values('username')[0].get('username')] = a.filter(user=i.get('user')).count()
    user_top = sorted(user_top.iteritems(), key=lambda d: d[1], reverse=True)
    date_list = getDaysByNum()
    for i in date_list:
        a = TaskLogDetail.objects.filter(date__year=i.year, date__month=i.month, date__day=i.day).count()
        detail_num.append(a)
    task_details_num = {'task_details_num': detail_num, }
    task_log = []
    tasks_num = {'tasks_num': TaskLog.objects.count(), }
    tasks = TaskLog.objects.filter(task_pid=0).order_by('-id')[:5]
    for task in tasks:
        tasks_dict = {'id': task.id, 'date': task.start_time, 'user': task.user.username, 'task_type': task.task_type, 'hosts': task.hosts.select_related().count(), 'business': task.task_business, 'finished_num': task.tasklogdetail.filter(result='ok').count(), 'failed_num': task.tasklogdetail.filter(result='failed').count(), 'unknown_num': task.tasklogdetail.filter(result='unknown').count(), 'content': task.task_content}
        task_log.append(tasks_dict)
    index_data.extend([users_num, task_details_num, user_top, ips, task_type_num, tasks_num, task_log])
    dash_data_list = json.dumps(index_data, default=json_date_handler)

    return HttpResponse(dash_data_list)
