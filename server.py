import json
import socket
from thread import *
from ansible_api import *
from rpyc import Service
from rpyc.utils.server import ThreadedServer


class ManagerService(Service):

    def exposed_login(self,user,passwd):

        if user=="ANuser" and passwd=="KJS23o4ij09gHF734iuhsdfhkGYSihoiwhj38u4h":
            self.Checkout_pass=True
        else:
            self.Checkout_pass=False

    def exposed_Runcommands(self,conn):

        self.data = conn
        recvData = eval(self.data)
        if recvData['task_type'] == '初始化及软件安装':
            push_resource = recvData['resource']
            task = MyTask(push_resource)
            if recvData['init_type'] == 'initalize':
                res = task.qd_initialize()
            elif recvData['init_type'] == 'php':
                res = task.qd_php()
            elif recvData['init_type'] == 'tomcat':
                res = task.qd_tomcat()
        elif recvData['task_type'] == 'root密码修改':
            push_resource, password, username = recvData['resource'], recvData['pass_new'], 'root'
            for i in push_resource:
                task = MyTask(i)
                pass_auth = task.passwd_auth
                if pass_auth == 'pong':
                    res = task.chan_root_pw(username, password_new)
                elif pass_auth == 'bad':
                    res = 'root密码错误,重新确认后再输入'
        else:
            push_resource, yml, upstreams, upstream, servers, server_ssls, locations = recvData['resource'], recvData['yml'], recvData['upstreams'], recvData['upstream'], recvData['servers'], recvData['server_ssls'], recvData['locations']
            for i in push_resource:
                task = MyTask(i)
                pass_auth = task.passwd_auth
                if pass_auth == 'pong':
                    task = App(i)
                    res = task.nginx_conf_deploy(yml, upstreams, upstream, servers, server_ssls, locations)
                    a = {}
                    a['mqqpass'] = i
                    res = dict(res, **a)

        print res
	    returnString = str(res)
        return returnString


s = ThreadedServer(ManagerService,port=28080,auto_register=False)
s.start()
