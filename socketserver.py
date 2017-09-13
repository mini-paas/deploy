#coding=utf-8

import json
import socket
from thread import *
from ansible_api import *


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address = ('',28080)
try:
    s.bind(address)
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)


def clientthread(conn):
    while True:
        data = conn.recv(8096)
        print data
        if len(data) <1637:
            break
        recvData = eval(data)
        #print recvData
        push_resource,yml,upstreams, upstream, servers, server_ssls, locations = recvData['resource'],recvData['yml'],recvData['upstreams'],recvData['upstream'],recvData['servers'],recvData['server_ssls'],recvData['locations']
        task = App(push_resource)
        res = task.nginx_conf_deploy(yml, upstreams, upstream, servers, server_ssls, locations)
        sendata = str(res)
        print sendata
        conn.sendall(sendata)
    conn.close()


while 1:
    conn, addr = s.accept()
    start_new_thread(clientthread ,(conn,))
    #clientthread(conn)
s.close()





'''
while True:
    newServerSocket,destAddr = tcpServerSocket.accept()
    while True:
        recv = newServerSocket.recv(102400)
	if recv:
            recvData = eval(recv)
	    if len(recvData)>0:
	        push_resource,yml,upstreams, upstream, servers, server_ssls, locations = recvData['resource'],recvData['yml'],recvData['upstreams'],recvData['upstream'],recvData['servers'],recvData['server_ssls'],recvData['locations']
	        task = App(push_resource)
    	        res = task.nginx_conf_deploy(yml, upstreams, upstream, servers, server_ssls, locations)
	        print res
                newServerSocket.send(str(res))
                #newServerSocket.close()
	    elif len(recvData) == 0:
                #newServerSocket.close()
                print('----------')
                break
    newServerSocket.close()
tcpServerSocket.close()
'''

def socketconnect(senddata):
    tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tcpClientSocket.connect(('10.173.25.36', 28080))
    while True:
        if len(senddata) > 0:
            tcpClientSocket.sendall(senddata)
        else:
            break
        time.sleep(2)
        recv = tcpClientSocket.recv(8096)
        print recv
        return eval(recv)
    tcpClientSocket.close()
