# coding:utf-8
from nginx_deploy.views import *
from deploy.models import *
from deploy.utils import *
from django.utils import timezone
from django.views.generic.list import ListView
import json
import os
import signal
import string


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


def hosts_multi(request):
    recent_tasks = TaskLog.objects.filter(task_pid=0).order_by('-id')[:5]
    return my_render('deploy/host_multi.html', locals(), request)


def hosts_multi_filetrans(request):
    random_str = ''.join(random.sample(string.ascii_lowercase, 8))
    #recent_tasks = TaskLog.objects.filter(task_user_id=1).order_by('-id')[:10]
    return my_render('deploy/hosts_multi_filetrans.html', locals(), request)


def list_create():
    a, d, b, e, g, c, f = 0, 0, [], [], [], {}, {}
    for i in Nginx_Group_Info.objects.all():
        d += 1
        f['text'] = str(i.groupname)
        f['id'] = d
        conf = Nginx_Info.objects.filter(group__groupname=str(i.groupname)).values('full_name')
        if conf:
            for cf in conf:
                a += 1
                c['text'] = cf.get('full_name')
                c['id'] = a
                b.append(c)
                f['child'] = b
                c = {}
            b = []
        else:
            f['child'] = []
        g.append(f)
        f = {}
    return g


def conf_list(request):
    conf_list = list_create()
    return HttpResponse(json.dumps(conf_list))


def task_list(request):
    tasklist = [{'id': 1, 'text': 'nginx配置发布', 'child': list_create()}, {'id': 2, 'text': '初始化', 'child': [{'id': 1, 'text': "起点中文", 'child': [{'id': 1, 'text': "initialize"},{'id': 2, 'text': "site"}, {'id': 3, 'text': "tomcat"}]},{'id': 2,'text': "创世中文", 'child': [ ]}, ]}, {'id': 3, 'text': 'root密码修改', 'child':[]},]

    return HttpResponse(json.dumps(tasklist))


def create_task_log(task_type, business, user, host_ids, content):
    l, l1, l2 = [], [], []
    l.append(user)
    l.sort(cmp)
    user_list = Users.objects.values('username')
    for i in user_list:
        username = i.get('username')
        l1.append(username)
    l1.sort(cmp)
    a = list(set(l) - set(l1))
    if a:
        Users(username=a[0]).save()

    host_ids.sort(cmp)
    ip_list = Hosts.objects.values('host_ip')
    for i in ip_list:
        ip = i.get('host_ip')
        l2.append(ip)
    l2.sort(cmp)
    b = list(set(host_ids) - set(l2))
    for ida in b:
        Hosts(host_ip=ida).save()

    user_name = Users.objects.get(username=user)
    if task_type == 'root密码修改':
        content, business = '', ''
        task_log_obj = TaskLog(task_type=task_type, task_content=content, task_business=business, user=user_name)
        task_log_obj.save()
    else:
        task_log_obj = TaskLog(task_type=task_type, task_content=content, task_business=business, user=user_name)
        task_log_obj.save()
    for h in host_ids:
        host = Hosts.objects.get(host_ip=h)
        task_log_obj.hosts.add(host)
        task_log_detail_obj = TaskLogDetail(child_of_task=task_log_obj, event_log='', host=host, result='unknown')
        task_log_detail_obj.save()
    return task_log_obj


def task_template_select(task_type, business, content, host_ids):
    global task_send
    task_resources = []
    if task_type == 'root密码修改':
        for i in host_ids:
            host = Hosts.objects.filter(host_ip=i)
            if not host:
                Hosts(host_ip=i).save()
            task_resource = gen_resource(i.encode('utf-8'), user='root', passwdold=business)
            task_resources.extend(task_resource)
        task_send = {'task_type': 'root密码修改', 'resource': task_resources, 'pass_new': content}
    elif task_type == 'nginx配置发布':
        for i in host_ids:
            host = Hosts.objects.filter(host_ip=i)
            if not host:
                Hosts(host_ip=i).save()
            host = Hosts.objects.get(host_ip=i)
            try:
                host_password = HostUsers.objects.filter(host=host, host_user='mqq').values('host_password')
            except:
                host_password = ''
            if host_password:
                password = CRYPTOR.decrypt(host_password[0]['host_password'])
                task_resource = gen_resource(i.encode('utf-8'), user='mqq', passwdold=password)
            else:
                task_resource = gen_resource(i.encode('utf-8'), user='mqq', passwdold=['mqq2005', 'Bluff@2015'])
            task_resources.extend(task_resource)
        nginx_infor_id = Nginx_Info.objects.filter(full_name=content).values('id')[0]['id']
        upstreams, upstream, servers, server_ssls, locations = nginxinfor_detail(nginx_infor_id)
        if business == 'QQ阅读':
            task_send = {'task_type': 'nginx配置发布', 'yml': 'nginx/nginx_deploy.yml', 'resource': task_resources, 'upstreams': upstreams, 'upstream': upstream, 'servers': servers, 'server_ssls': server_ssls, 'locations': locations}
        elif business == '起点中文':
            task_send = {'task_type': 'nginx配置发布', 'yml': 'nginx/nginx_deploy_qidian.yml', 'resource': task_resources, 'upstreams': upstreams, 'upstream': upstream, 'servers': servers, 'server_ssls': server_ssls, 'locations': locations}
    elif task_type == '初始化':
        for i in host_ids:
            host = Hosts.objects.filter(host_ip=i)
            if not host:
                Hosts(host_ip=i).save()
            host = Hosts.objects.get(host_ip=i)
            host_password = HostUsers.objects.filter(host=host, host_user='root').values('host_password')
            password = CRYPTOR.decrypt(host_password[0]['host_password'])
            task_resource = gen_resource(i.encode('utf-8'), user='root', passwdold=password)
            task_resources.extend(task_resource)
        if business == '起点中文':
            task_send = {'task_type': '初始化', 'resource': task_resources, 'task_business': business, 'init_type': content}
        elif business == '创世中文':
            task_send = {'task_type': '初始化', 'resource': task_resources, 'task_business': business, 'init_type': content}
    elif task_type == '自定义任务':
        for i in host_ids:
            host = Hosts.objects.filter(host_ip=i)
            if not host:
                Hosts(host_ip=i).save()
            host = Hosts.objects.get(host_ip=i)
            host_password = HostUsers.objects.filter(host=host, host_user='root').values('host_password')
            password = CRYPTOR.decrypt(host_password[0]['host_password'])
            task_resource = gen_resource(i.encode('utf-8'), user='root', passwdold=password)
            task_resources.extend(task_resource)
        task_send = {'task_type': '命令执行', 'resource': task_resources, 'command': content}
    elif task_type == '文件下发' or task_type == '文件回收':
        for i in host_ids:
            host = Hosts.objects.filter(host_ip=i)
            if not host:
                Hosts(host_ip=i).save()
            host = Hosts.objects.get(host_ip=i)
            host_password = HostUsers.objects.filter(host=host, host_user='root').values('host_password')
            password = CRYPTOR.decrypt(host_password[0]['host_password'])
            task_resource = gen_resource(i.encode('utf-8'), user='root', passwdold=password)
            task_resources.extend(task_resource)
        task_send = {'task_type': task_type, 'resource': task_resources, 'file_path': business, 'target_path': content}
    return task_send


def passwd_check(res):
    try:
        res['mqqpass']
    except:
        res['mqqpass'] = ''
    if res['mqqpass']:
        content = CRYPTOR.encrypt(res['mqqpass']['password'])
        HostUsers(host=Hosts.objects.get(host_ip=res['mqqpass']['ip']), host_user=res['mqqpass']['username'], host_password=content).save()
    try:
        res['root']
    except:
        res['root'] = ''
    if res['root']:
        content_save = CRYPTOR.encrypt(res['root']['password'])
        host = Hosts.objects.get(host_ip=res['root']['ip'])
        try:
            host_password = HostUsers.objects.filter(host=host, host_user='root').values('host_password')
        except:
            host_password = ''
        if host_password:
            HostUsers.objects.filter(host=host, host_user='root').update(host_password=content_save)
        else:
            HostUsers(host=host, host_user='root', host_password=content_save).save()


def task_action(request):
    cmd = request.POST.get('cmd')
    #host_ids = request.POST.get('selected_hosts')
    host_ids = ['10.173.25.36']
    #cmd, host_ids = json.loads(cmd), json.loads(host_ids)
    cmd = json.loads(cmd)
    task_type = cmd['first']['text']
    business = cmd['second']['text']
    content = cmd['third']['text']
    if task_type == '自定义任务':
       task_name = cmd['four']['text']
       business = business + '-' + task_name
    user = request.COOKIES.get('bk_uid')
    task_obj = create_task_log(task_type, business, user, host_ids, content)
    send = task_template_select(task_type, business, content, host_ids)
    senddata = str(send)
    conn = rpyc.connect('10.173.25.36', 28080)
    conn.root.login('ANuser', 'KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    res = conn.root.Runcommands(senddata)
    res = eval(res)
    passwd_check(res)
    task_id = task_obj.id
    log_obj = TaskLogDetail.objects.get(child_of_task_id=int(task_id))
    resstatus_ok, resstatus_failed = res['ok'], res['failed']
    for key, value in resstatus_ok.items():
        if log_obj.host == Hosts.objects.get(host_ip=key):
            log_obj.event_log = value
            log_obj.result = 'ok'
            log_obj.save()
    for key, value in resstatus_failed.items():
        if log_obj.host == Hosts.objects.get(host_ip=key):
            log_obj.event_log = value
            log_obj.result = 'failed'
            log_obj.save()
    if task_id:
        return HttpResponse(task_id)
    else:
        return HttpResponse("TaskCreatingError")


def task_res(request, detail=True):
    task_id = request.GET.get('task_id')
    log_dic = {'detail': {}}
    task_obj = TaskLog.objects.get(id=int(task_id))
    task_detail_obj_list = TaskLogDetail.objects.filter(child_of_task_id=task_obj.id)
    log_dic['summary'] = {'id': task_obj.id, 'start_time': task_obj.start_time, 'task_type': task_obj.task_type, 'task_business':task_obj.task_business, 'host_num': task_obj.hosts.select_related().count(), 'finished_num': task_detail_obj_list.filter(result='ok').count(), 'failed_num': task_detail_obj_list.filter(result='failed').count(), 'unknown_num': task_detail_obj_list.filter(result='unknown').count(), 'content': task_obj.task_content}
    if detail:
        for log in task_detail_obj_list:
            log_dic['detail'][log.id] = {'date': log.date, 'username': log.child_of_task.user.username, 'host_id': log.host.id, 'ip_addr': log.host.host_ip, 'event_log': log.event_log, 'result': log.result}

    task_result = json.dumps(log_dic, default=json_date_handler)
    return HttpResponse(task_result)


def task_log_detail(request):
    task_id = request.GET.get('id')
    return my_render('deploy/multi_task_log.html', locals(), request)


def task_abort(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        assert task_id.isdigit()
        task_obj = TaskLog.objects.get(id=int(task_id))
        try:
            os.killpg(task_obj.task_pid, signal.SIGTERM)
            res_msg = 'Task %s has terminated!' % task_id
        except OSError as e:
            res_msg = "Error happened when tries to terminate task %s , err_msg[%s]" % (task_id, str(e))
        return HttpResponse(json.dumps(res_msg))


def user_audit(request, user_id):
    user_list = Users.objects.all()
    user = Users.objects.get(id=int(user_id))
    user_multi_task_records = TaskLog.objects.filter(user=user).filter(task_pid=0).order_by('-start_time')
    user_task_list, p, user_multi_task_record, page_range, current_page, show_first, show_end = pages(user_multi_task_records, request)

    return my_render('deploy/yw_user.html', locals(), request)


def handle_upload_file(request, random_str, response_dic):
    upload_dir = '%s/task_data/tmp/%s' % (FileUploadDir, random_str)
    for k, file_obj in request.FILES.items():
        filename = '%s/%s' % (upload_dir, file_obj.name)
        if len(os.listdir(upload_dir)) <= MaxUploadFiles:
            with open(filename, 'wb') as destination:
                f = File(destination)
                storage.save(filename, f)
        else:
            response_dic['error'] = "can only upload no more than %s files." % (MaxUploadFiles,)


def task_file_upload(request):
    random_str = ''.join(random.sample(string.ascii_lowercase, 8))
    upload_dir = "%s/task_data/tmp/%s" % (FileUploadDir, random_str)
    response_dic = {'files': {}}
    user = request.COOKIES.get('bk_uid')
    l, l1, l2 = [], [], []
    l.append(user)
    l.sort(cmp)
    user_list = Users.objects.values('username')
    for i in user_list:
        username = i.get('username')
        l1.append(username)
    l1.sort(cmp)
    a = list(set(l) - set(l1))
    if a:
        Users(username=a[0]).save()
    user_name = Users.objects.get(username=user)
    for k, file_obj in request.FILES.items():
        filename = '%s/%s' % (upload_dir, file_obj.name)
        with NamedTemporaryFile() as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
            f = File(destination)
            storage.save(filename, f)
        size = storage.size(filename)
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        FileList(file_name=file_obj.name, file_size=size, file_create_time=ctime, user=user_name, files_dir=random_str).save()
    filelist = FileList.objects.filter(user=user_name)
    for file in filelist:
        response_dic['files'][file.id] = {'file_name': file.file_name, 'user': file.user.username, 'file_create_time': file.file_create_time, 'file_size': file.file_size, 'files_dir': file.files_dir}
    return HttpResponse(json.dumps(response_dic))


def delete_file(request, random_str):
    response, file_abs = {}, ''
    if request.method == "POST":
        upload_dir = "%s/task_data/tmp/%s" % (FileUploadDir, random_str)
        filename = request.POST.get('filename')
        file_id = request.POST.get('fileid')
        if filename and file_id:
            file_abs = "%s/%s" % (upload_dir, filename.strip())
        if storage.exists(file_abs):
            storage.delete(file_abs)
            FileList.objects.filter(id=file_id).delete()
            response['msg'] = "file '%s' got deleted " % filename
        else:
            response["error"] = "file '%s' does not exist on server" % filename
    return HttpResponse(json.dumps(response))


def send_zipfile(request, file_path, file_name):
    zip_file_name = '%s_files' % file_name
    archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    file__name = file_name.encode('utf-8')
    filepath = storage.url('%s/%s' % (file_path, file__name.strip()))
    file_path = urllib.unquote(filepath.encode('utf-8'))
    bash('curl -O %s' % file_path)
    if os.path.isfile(file__name):
        archive.write(file__name, arcname=file__name)
        archive.close()
    wrapper = FileWrapper(open(zip_file_name, 'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % (urlquote(zip_file_name))
    response['Content-Length'] = os.path.getsize(zip_file_name)
    return response


def file_download(request, random_str):
    file_path, file_name = '', ''
    if request.method == "POST":
        file_path = "%s/task_data/tmp/%s" % (FileUploadDir, random_str)
        file_name = request.POST.get('filename')
    return send_zipfile(request, file_path, file_name)


def task_file(request):
    cmd = request.POST.get('cmd')
    host_ids = request.POST.get('selected_hosts')
    cmd, host_ids = json.loads(cmd), json.loads(host_ids)
    task_type = cmd['first']['text']
    business = cmd['second']['text']
    remote_file_path = cmd['third']['text']
    user = request.COOKIES.get('bk_uid')
    local_file_list = os.listdir("%s/task_data/tmp/%s" % (FileUploadDir, business))
    local_file_list = storage.url(local_file_list)
    content = "send local files %s to remote path [%s]" % (local_file_list, remote_file_path)
    task_obj = create_task_log(task_type, user, host_ids, business, content)
    send = task_template_select(task_type, local_file_list, remote_file_path, host_ids)
    senddata = str(send)
    conn = rpyc.connect('10.173.25.36', 28080)
    conn.root.login('ANuser', 'KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h')
    res = conn.root.Runcommands(senddata)
    res = eval(res)
    task_id = task_obj.id
    log_obj = TaskLogDetail.objects.get(child_of_task_id=int(task_id))
    resstatus_ok, resstatus_failed = res['ok'], res['failed']
    for key, value in resstatus_ok.items():
        if log_obj.host == Hosts.objects.get(host_ip=key):
            log_obj.event_log = value
            log_obj.result = 'ok'
            log_obj.save()
    for key, value in resstatus_failed.items():
        if log_obj.host == Hosts.objects.get(host_ip=key):
            log_obj.event_log = value
            log_obj.result = 'failed'
            log_obj.save()
    if task_id:
        return HttpResponse(task_id)
    else:
        return HttpResponse("TaskCreatingError")


class define_tasks(View):

    def delete(self, request):
        task_ids = request.GET.get('id')
        print task_ids
        task_id_list = task_ids.split(',')
        for task_id in task_id_list:
            TaskLog.objects.filter(id=task_id).delete()

        return HttpResponse(u"del success!")

    def post(self, request):
        user = request.COOKIES.get('bk_uid')
        user_name = Users.objects.get(username=user)
        cmd = request.POST.get('cmd')
        host_ids = request.POST.get('selected_hosts')
        cmd, host_ids = json.loads(cmd), json.loads(host_ids)
        task_type = cmd['first']['text']
        business = cmd['second']['text']
        content = cmd['third']['text']
        l, l1, l2 = [], [], []
        l.append(user)
        l.sort(cmp)
        user_list = Users.objects.values('username')
        for i in user_list:
            username = i.get('username')
            l1.append(username)
        l1.sort(cmp)
        a = list(set(l) - set(l1))
        if a:
            Users(username=a[0]).save()
        host_ids.sort(cmp)
        ip_list = Hosts.objects.values('host_ip')
        for i in ip_list:
            ip = i.get('host_ip')
            l2.append(ip)
        l2.sort(cmp)
        b = list(set(host_ids) - set(l2))
        for ida in b:
            Hosts(host_ip=ida).save()
        task_log_obj = TaskLog(task_type=task_type, task_content=content, task_business=business, user=user_name, task_pid=1)
        task_log_obj.save()
        for h in host_ids:
            host = Hosts.objects.get(host_ip=h)
            task_log_obj.hosts.add(host)

        return HttpResponse(u"task create success!")

    def get(self, request):
        task_log, tasks = [], ''
        user = request.COOKIES.get('bk_uid')
        # if user == 'p_zywzhang' or user == 'p_nnanli' or user == 'p_andyhan':
        #     tasks = TaskLog.objects.filter(task_type='自定义任务').filter(task_pid=1).order_by('-id')
        # else:
        l, l1 = [], []
        l.append(user)
        l.sort(cmp)
        user_list = Users.objects.values('username')
        for i in user_list:
            username = i.get('username')
            l1.append(username)
        l1.sort(cmp)
        a = list(set(l) - set(l1))
        if a:
            Users(username=a[0]).save()
        user_name = Users.objects.get(username=user)
        tasks = TaskLog.objects.filter(user=user_name).filter(task_type='自定义任务').filter(task_pid=1).order_by('-id')
        for task in tasks:
            ip_list = task.hosts.values('host_ip')
            a = []
            for i in ip_list:
                b = i.get('host_ip').encode('utf-8')
                a.append(b)
            tasks_dict = {'id': task.id, 'user': task.user.username, 'task_type': task.task_type, 'hosts_num': task.hosts.select_related().count(), 'hosts': a, 'business': task.task_business, 'content': task.task_content}
            task_log.append(tasks_dict)
        recent_tasks_list = json.dumps(task_log, default=json_date_handler)

        return HttpResponse(recent_tasks_list)

    def put(self, request):
        put = QueryDict(request.body, encoding=request.encoding)
        cmd, host_ids = put.get('cmd'), put.get('selected_hosts')
        cmd, host_ids = json.loads(cmd), json.loads(host_ids)
        task_type = cmd['first']['text']
        business = cmd['second']['text']
        content = cmd['third']['text']
        l2 = []
        host_ids.sort(cmp)
        ip_list = Hosts.objects.values('host_ip')
        for i in ip_list:
            ip = i.get('host_ip')
            l2.append(ip)
        l2.sort(cmp)
        b = list(set(host_ids) - set(l2))
        for ida in b:
            Hosts(host_ip=ida).save()
        TaskLog.objects.filter(id=put.get('id')).update(task_type=task_type, task_content=content, task_business=business)
        task_log_obj = TaskLog.objects.get(id=put.get('id'))
        task_log_obj.hosts.clear()
        for h in host_ids:
            host = Hosts.objects.get(host_ip=h)
            task_log_obj.hosts.add(host)

        return HttpResponse(u"task update success!")


def define_task_list(request):

    return my_render('deploy/hosts_multi_filetrans_list.html', locals(), request)


# class TaskLogListView(ListView):
#     model = TaskLog
#     context_object_name = 'tasklog_list'
#     template_name = 'deploy/hosts_multi_filetrans_list.html'
#
#     def get_context_data(self, **kwargs):
#         tasks = TaskLog.objects.filter(task_type='自定义任务').order_by('-id')
#         context = {
#             'tasks': tasks
#         }
#         kwargs.update(context)
#         return super(TaskLogListView, self).get_context_data(**kwargs)
#         # context = super(TaskLogListView, self).get_context_data(**kwargs)
#         # context['now'] = timezone.now()
#         # return context


# class TaskLogCreateView(CreateView):
#     model = TaskLog
#     form_class = forms.AssetCreateForm
#     template_name = 'assets/asset_create.html'
#     success_url = reverse_lazy('assets:asset-list')
#
#     def form_valid(self, form):
#         self.asset = asset = form.save()
#         asset.created_by = self.request.user.username or 'Admin'
#         asset.date_created = timezone.now()
#         asset.save()
#         return super(TaskLogCreateView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'app': 'Assets',
#             'action': 'Create asset',
#         }
#         kwargs.update(context)
#         return super(TaskLogCreateView, self).get_context_data(**kwargs)
#
#     def get_success_url(self):
#         update_assets_hardware_info.delay([self.asset._to_secret_json()])
#         return super(TaskLogCreateView, self).get_success_url()
#
#
# class TaskLogDetailView(DetailView):
#     model = TaskLog
#     context_object_name = 'tasklog_detail'
#     template_name = 'assets/asset_detail.html'
#
#     def get_context_data(self, **kwargs):
#         asset_groups = self.object.groups.all()
#         system_users = self.object.system_users.all()
#         context = {
#             'app': 'Assets',
#             'action': 'Asset detail',
#             'asset_groups_remain': [asset_group for asset_group in AssetGroup.objects.all()
#                                     if asset_group not in asset_groups],
#             'asset_groups': asset_groups,
#             'system_users_remain': [system_user for system_user in SystemUser.objects.all()
#                                     if system_user not in system_users],
#             'system_users': system_users,
#         }
#         kwargs.update(context)
#         return super(TaskLogDetailView, self).get_context_data(**kwargs)
#
#
# class TaskLogUpdateView(UpdateView):
#     model = TaskLog
#     form_class = forms.AssetUpdateForm
#     template_name = 'assets/asset_update.html'
#     success_url = reverse_lazy('assets:asset-list')
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'app': 'Assets',
#             'action': 'Update asset',
#         }
#         kwargs.update(context)
#         return super(TaskLogUpdateView, self).get_context_data(**kwargs)
#
#     def form_invalid(self, form):
#         print(form.errors)
#         return super(TaskLogUpdateView, self).form_invalid(form)
#
#
# class TaskLogDeleteView(DeleteView):
#     model = TaskLog
#     template_name = 'assets/delete_confirm.html'
#     success_url = reverse_lazy('assets:asset-list')
