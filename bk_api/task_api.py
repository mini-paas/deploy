# -*- coding: utf-8 -*-
"""
@author: daxwang
@date: 2014-02-26
@summary: 与Task相关的接口封装,如果你需要对此处的函数做进一步的封装或改动, 请放到其他文件中, 保持此文件不改动, 就可以方便后续框架更新时, 此文件即可直接覆盖升级.
"""
import json
import re

from bk_api.utils import http_request_workbench
from bk_api.settings_bk import BK_URL, SITE_URL, RUN_MODE, logger

# POST请求
URL_TASK_CREATE = '%s/task/api/create_single_task/' % BK_URL
URL_TASK_EXECUTE = '%s/task/api/execute_task/' % BK_URL
URL_TASK_PAUSE = '%s/task/api/pause_task/' % BK_URL
URL_TASK_RESUME = '%s/task/api/resume_task/' % BK_URL
URL_REVOKE_SCHEDULE_TASK = '%s/task/api/revoke_schedule_task/' % BK_URL
URL_SETUP_NODE_ORDER = '%s/task/api/setup_node_order/' % BK_URL
URL_TASKS_DELETE = '%s/task/api/delete_tasks/' % BK_URL
URL_CONTEXT_SET = '%s/task/api/set_context/' % BK_URL
URL_TERMINATE_TASK = '%s/task/api/terminate_task/' % BK_URL  # 终止任务url
# GET请求
URL_EVENT_FLOW = '%s/task/api/get_event_flow/' % BK_URL
URL_TASKS = '%s/task/api/tasks_list/' % BK_URL
URL_RECORDS = '%s/task/api/task_records/' % BK_URL
URL_RECORD = '%s/task/api/task_record/' % BK_URL
URL_LOGS = '%s/task/api/task_logs/' % BK_URL
URL_EXE_INFO = '%s/task/api/get_task_executing_info/' % BK_URL
URL_CONTEXT_GET = '%s/task/api/get_context/' % BK_URL

REGEX_NODE_ORDER = re.compile(r'^\w+(=>\w+)*$')

DEFAULT_TASK_URL_FORMAT = SITE_URL + 'task/%s/'  # 此处%s代表task_id的位置
DEFAULT_RECORD_URL_FORMAT = SITE_URL + 'record/%s/'  # 此处%s代表task_id位置


def remote_create_single_task(event_flow, task_name, app_code, external_url_format, username, **kwargs):
    '''
            调用蓝鲸远程服务，创建任务并返回Task_id
    @param event_flow: 事件流程编码
    @param task_name: 任务名称
    @param app_code: 应用编码
    @param external_url_format: 本地task详情页面的url的格式, 类似'/my_appcode/task/%s/', 推荐传入
                                若确实没有task详情页面, 则传入None或空字符串
    @param username: 创建者的用户名
    @param kwargs：可选参数，包括：
        {
            operate_type(可选): 任务的操作类型 (没有明确操作类型, 则不传或传None)
                                   ('KQ', u"开区类"),
                                   ('KR', u"扩容类"),
                                   ('XJ', u"下架类"),
                                   ('FB', u"发布类"),
                                   ('LC', u"流程类"),
                                   ('GZCL', u"故障处理类")
            cc_biz_id(可选): 对应的CC业务的id (用于统计的可选参数, 不传则为0)
            node_order(可选): 筛选后的流程节点顺序 (可选, 如果不传或者传None则执行全部节点,
                            如果传则必须符合格式要求, 比如: "aaa=>bbb=>ccc")
            operators(可选)：任务操作者集合，多个以逗号分隔，如(daxwang,huifu,sundytian),operators不传或者传入None，则表示任何人都可以操作该任务。
            schedule_time(可选)：定时任务定时时间，非定时任务不传或者传入None
            task_notify_url(可选)：回调函数url，没有不回调函数时，不传或者传入None
        }

    @return {'result': True/False, 'message':附加信息}
            如果成功,message即为新建好的task_id, 稍后根据此id来查询状态和结果, 否则为错误信息
    '''
    try:
        post_task = {
            "event_flow": event_flow,
            'task_name': task_name,
            'app_code': app_code,
            'external_url_format': external_url_format or DEFAULT_TASK_URL_FORMAT,
            'username': username,
        }

        # 检查加入可选参数
        if 'operate_type' in kwargs:
            post_task['operate_type'] = kwargs['operate_type']
        if 'cc_biz_id' in kwargs:
            post_task['cc_biz_id'] = kwargs['cc_biz_id']
        if 'node_order' in kwargs:
            node_order = kwargs['node_order']
            _check = _check_node_order(node_order)  # 如果传入了node_order则必须符合格式要求
            if _check['result']:
                post_task['node_order'] = node_order  # 加入post参数
            else:
                return _check  # 直接返回错误信息
        # 定时
        if 'schedule_time' in kwargs:
            post_task['schedule_time'] = kwargs['schedule_time']
        # 回调url
        if 'task_notify_url' in kwargs:
            post_task['task_notify_url'] = kwargs['task_notify_url']

        resp = http_request_workbench(URL_TASK_CREATE, 'POST', post_task)
        if resp['result']:
            return {'result': True, 'message': resp['message']['task_id']}
        else:
            logger.error(resp['message'])
            return {'result': False, 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_execute_task(task_id, params_dict, username, **kwargs):
    '''
    调用蓝鲸远程服务，通知L2任务执行后台开始执行任务
    (注意这里只是开始执行, 任务执行可能会用时几秒到几天, 执行结果需要另外查询)

    @param task_id: 任务id
    @param params_dict: 任务执行所需的参数字典, 参数组装格式为字典,
                        key为执行流程中各个节点的名称, value为该节点所需要的参数, 比如:
                        {
                            'global': data, #global参数里放置公用参数, 所有其他节点都可以从其中取值
                            'node_1': node_1_param, #节点参数请参考(http://t.open.oa.com/component/doc/)
                            'node_2': data_2_param,
                            'node_xxx': ....
                        }
                        组装过程可参考test_app_l123/views.py中的_build_kaiqu_params函数
    @param username: 操作人的用户名
    @param kwargs:可选参数，包括：
        {
            schedule_time(可选): 指定时间开始执行任务(请传入北京时间 '%Y-%m-%d %H:%M')
                                        注:schedule_time参数已经移到remote_create_single_task方法中（建议将schedule_time作为remote_create_single_task的参数传入），这里保留是为了兼容以前版本。
            ignore_cur_node_err(可选) 是否忽略当前节点错误继续执行, 0/不忽略; 1/忽略，不传默认为0
            totally_restart(可选): 废弃当前任务, 完全彻底地从头重新开始执行当前任务
                                  0/不重新执行; 1/完全重新执行 (只允许在出错情况下使用),不传默认为0
        }

    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        param_json = json.dumps(params_dict)
        post_exe = {
            "task_id": task_id,
            "param_json": param_json,
            'username': username,
        }
        # 检查加入可选参数
        if 'ignore_cur_node_err' in kwargs:
            post_exe['ignore_cur_node_err'] = kwargs['ignore_cur_node_err']
        if 'totally_restart' in kwargs:
            post_exe['totally_restart'] = kwargs['totally_restart']
        resp = http_request_workbench(URL_TASK_EXECUTE, 'POST', post_exe)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_pause_task(task_id, username):
    '''
    调用蓝鲸远程服务，暂停正在执行的任务
    @param task_id: 任务id
    @param username: 操作人的用户名
    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        post_pause = {
            "task_id": task_id,
            'username': username,
        }
        resp = http_request_workbench(URL_TASK_PAUSE, 'POST', post_pause)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_resume_task(task_id, username):
    '''通知蓝鲸任务引擎: 执行暂停或失败状态下的任务(不保存执行参数)
    @param task_id: 任务id
    @param username: 操作人的用户名
    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        post_resume = {
            "task_id": task_id,
            'username': username,
        }
        resp = http_request_workbench(URL_TASK_RESUME, 'POST', post_resume)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u'调用蓝鲸远程服务失败，错误信息:%s' % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_setup_node_order(task_id, username, node_order=None):
    '''
            设定流程节点顺序 (必须在执行前设定, 一旦开始执行就固定了)
            此接口用于在创建一个没有筛选节点的任务后, 进行筛选节点操作,
            提交后让下个步骤的人只能做执行操作 (唯有执行参数还可以改)
    @param task_id: 任务id
    @param username: 操作人的用户名
    @param node_order(可选): 筛选过的流程节点顺序, 如果不传或者传None则执行全部节点,
                             如果传则必须符合格式要求, 比如: "aaa=>bbb=>ccc")
    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        post_setup = {
            "task_id": task_id,
            'username': username,
        }

        # 检查可选参数
        if node_order:
            _check = _check_node_order(node_order)  # 如果传入了node_order则必须符合格式要求
            if _check['result']:
                post_setup['node_order'] = node_order  # 加入post参数
            else:
                return _check  # 直接返回错误信息

        resp = http_request_workbench(URL_SETUP_NODE_ORDER, 'POST', post_setup)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_event_flow(event_flow):
    '''
            根据事件流程编码获取事件流程节点列表
            注: 组装节点顺序时格式要求: "aaa=>bbb=>ccc=>..."
    @param event_flow: 事件流程编码
    @return {'result': True/False, 'message':[{"brief_introduction": "获取服务器资源",
                                               "name": "res",
                                               "title": "获取资源"},
                                               ...]
            }
    '''
    try:
        url = URL_EVENT_FLOW + event_flow + '/'
        get = {
            'data_type': 'json',
        }

        resp = http_request_workbench(url, 'GET', get)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u'调用蓝鲸远程服务失败，错误信息:%s' % e}


def remote_get_tasks(app_code, record_url_format=None, filter_kwargs=None):
    '''
            根据应用编码和其他过滤条件来搜索任务列表
    @param app_code: 任务的相应应用编码
    @param record_url_format(可选): 本地的任务完成记录页面的url格式, 用于显示, 比如/record/%s/ (%s为taskid占位)
                                    如果你的Task不需要记录功能, 则不传
    @param filter_kwargs(可选): 更多过滤条件(可选参数), 传入字典, 格式如下
                                {'event_flow': 'aaa,bbbb' , ----根据流程来过滤, 支持用逗号分隔查多个流程
                                 'cc_biz_id': 123, ----所属CC业务id
                                 'operate_type': 'KQ', ----操作类型
                                 'status': 1/2/3/4, ----执行状态
                                }
                                注: 已自动加入RUN_MODE参数
    @return {'result': True/False, 'message': [ { "status": 6,
                                                  "status_msg": 状态码的说明
                                                  "create_time": "2012-11-09 16:11:49",
                                                  "name": "demo",
                                                  "cc_biz_name": "QXZB",
                                                  "creator": "mattsu",
                                                  "operate_type": "开区类",
                                                  "event_flow": 任务的流程定义
                                                  "id": 940,
                                                  "external_url": "/test_app_l123/task/940/",
                                                  "execute_time": 开始执行时间
                                                  "finish_time": 完成时间},
                                                 ...]
    '''
    try:
        url = URL_TASKS + app_code + '/'
        get = {
            'data_type': 'json',
            'record_url_format': record_url_format or DEFAULT_RECORD_URL_FORMAT,
        }
        if not filter_kwargs:
            filter_kwargs = {}
        filter_kwargs['RUN_MODE'] = RUN_MODE
        get['filter_kwargs'] = json.dumps(filter_kwargs)

        resp = http_request_workbench(url, 'GET', get)
        return {'result': resp['result'], 'message': resp['data']['tasks']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_tasks_by_ids(task_ids):
    '''
            根据任务的id数组来获取任务列表
    @param task_ids: task_id的数组
    @return {'result': True/False, 'message': 字段格式与remote_get_tasks相同}
    '''
    try:
        get = {
            'task_ids': ','.join(map(str, task_ids)),  # 用map把int转成str
        }
        resp = http_request_workbench(URL_TASKS, 'GET', get)
        return {'result': resp['result'], 'message': resp['data']['tasks']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_task_executing_info(task_id):
    '''
            获取一个任务的详细执行状态信息, 包括当前所有步骤的状态信息
    @return {'result': True/False, 'message':任务执行信息对象(如下)}
                        {'node_list':[node1, node2, ...],  # 步骤(流程)列表
                         'status':status,        # 任务状态码
                         'status_msg':           # 任务状态码对应的信息
                         'message':message,      # 任务消息
                         'duration':duration,    # 执行耗时
                         'execute_time': _task.execute_time or u'无记录',
                         'finish_time': _task.finish_time or u'无记录'
            }

            其中每个node节点的数据格式:
                {'status': 3,  # 节点状态码
                 'status_msg': # 节点状态码对应的信息
                 'name': u'res',  #流程中定义的节点名称
                 'data': u'{}',   #组件返回的callback数据(字符串格式, 需json解析)
                 'title': u'...', #节点标题
                 'brief_introduction': u'...',
                 'start_time': u'',  #开始时间
                 'end_time': u'2012-11-23 12:11:34', #节点结束执行时间
                 'duration': u'6s',  # 节点耗时
                 'message': u'GDB:192.168.0.0' # 节点的消息
                 }
    '''
    try:
        url = URL_EXE_INFO + str(task_id) + '/0/'
        resp = http_request_workbench(url, 'GET', None)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_delete_tasks_by_ids(task_ids):
    '''
            根据任务的id数组来删除任务(注意:只有状态为未执行的才会删除)
    @param task_ids: task_id的数组
    @return {'result': True/False,
             'message':[111,222,...] (成功删除了的id, 其他的id由于不存在或条件限制没有删除)
             }
    '''
    try:
        post = {
            'task_ids': ','.join(map(str, task_ids)),  # 用map把int转成str
        }
        resp = http_request_workbench(URL_TASKS_DELETE, 'POST', post)
        return {'result': resp['result'], 'message': resp['data']['tasks']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_records_by_app_optype(app_code, operate_type=None):
    '''
            获取一个App下的一种操作类型的所有任务的完成记录列表, 记录对象因操作类型不同而不同.
    @param app_code: 任务的相应应用编码
    @param operate_type: 任务的操作类型(可选参数)
    @return {'result': True/False, 'message':记录对象列表(因操作类型不同而不同, 如下:)}
                            [{
                               'result': 原始结果数据(最后一个步骤的data)
                               'time':   记录时间
                               'cc_biz_name': 任务所属CC业务名称
                               'task_id': 任务的id
                               'external_url': 任务详情链接
                               -------------------------------------
                               开区类任务的完成记录的额外字段:
                                'user': 操作者
                                'set_name': 大区名
                                'module_list': [{'name':模块名, 'ip_list':[ip1, ip2, ...]}, ...]
                               -------------------------------------
                               },
                               ...]
    '''
    try:
        get = {
            'data_type': 'json',
            'app_code': app_code,
        }
        if operate_type:
            get['operate_type'] = operate_type

        resp = http_request_workbench(URL_RECORDS, 'GET', get)
        return {'result': resp['result'], 'message': resp['data']}
    except Exception as e:
        logger.error(u'调用蓝鲸远程服务失败，错误信息:%s' % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_record_by_task(task_id):
    '''
            获取单个任务的完成记录,记录对象因操作类型不同而不同.
    @注意: 必须是已经执行成功的任务才有完成记录, 否则返回false
    @param task_id: 任务id
    @return {'result': True/False, 'message':记录对象(因操作类型不同而不同, 格式请参考remote_get_records_by_app_optype)}
    '''
    try:
        get = {
            'data_type': 'json',
            'task_id': task_id,
        }

        resp = http_request_workbench(URL_RECORD, 'GET', get)
        if resp['data']:
            return {'result': resp['result'], 'message': resp['data'][0]}
        else:
            logger.error(u"该任务(id:%s)没有完成记录, 可能没有执行成功, 请检查" % task_id)
            return {'result': False,
                    'message': u"该任务(id:%s)没有完成记录, 可能没有执行成功, 请检查" % task_id}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_task_logs(task_id):
    '''
            获取单个任务的执行日志
    @param task_id: 任务id
    @return {'result': True/False, 'message':日志列表(如下)}
                {[
                    {'task_id': ,
                     'operator': 操作者,
                     'start_time': 操作时间,
                     'user_action': 操作,
                     'status': 操作结果状态,
                     'message': 操作结果信息,
                     'task_param':任务执行时的参数
                     },

                     ...
                 ]}
    '''
    try:
        get = {
            'data_type': 'json',
            'task_id': task_id,
        }

        resp = http_request_workbench(URL_LOGS, 'GET', get)
        if resp['data']:
            return {'result': resp['result'], 'message': resp['data']}
        else:
            logger.error(u"该任务(id:%s)没有执行日志, 请检查!" % task_id)
            return {'result': False,
                    'message': u"该任务(id:%s)没有执行日志, 请检查!" % task_id}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_get_context(task_id, key_or_list, strict=False):
    '''
            获取第二层参数, 详细信息请参考第二层接口(http://10.130.73.106:12345/service/)里的context.get方法
    @param key_or_list: 单个key，或者key的列表(用逗号分隔)。  样例：'ijobs_xxx.ijobs_taski_id,global.operator'
    @return {'result': True/False, 'message': 获取到的key-value 对}
    '''
    try:
        get = {
            'task_id': task_id,
            'key_or_list': key_or_list,
            'strict': 1 if strict else 0,
        }

        resp = http_request_workbench(URL_CONTEXT_GET, 'GET', get)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_set_context(task_id, key_value_pair):
    '''
            修改第二层参数, 详细信息请参考第二层接口(http://10.130.73.106:12345/service/)里的context.set方法
    @param key_value_pair: 要修改的键值对的字典。  样例：{'ijobs_xxx.ijobs_taski_id':5000}
    @return {'result': True/False, 'message': 写入是否成功}
    '''
    try:
        post = {
            'task_id': task_id,
            'key_value_pair': json.dumps(key_value_pair)
        }

        resp = http_request_workbench(URL_CONTEXT_SET, 'POST', post)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def _check_node_order(node_order):
    '''检查不为空的node_order是否符合格式要求, 格式样例: "aaa=>bbb=>ccc"  '''
    if node_order is not None and not REGEX_NODE_ORDER.match(node_order):
        logger.error(u"自选节点参数(node_order)格式不正确(必须符合正则 '^\w+(=>\w+)*$' ), 而传入的是'%s'" % node_order)
        return {'result': False, 'message':
                u"自选节点参数(node_order)格式不正确(必须符合正则 '^\w+(=>\w+)*$' ), 而传入的是'%s'" % node_order}
    else:
        return {'result': True}


def remote_revoke_schedule_task(task_id, username):
    '''
            终止定时任务
    @param task_id: 任务id
    @param username: 操作人的用户名
    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        post_resume = {
            "task_id": task_id,
            'username': username,
        }
        resp = http_request_workbench(URL_REVOKE_SCHEDULE_TASK, 'POST', post_resume)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}


def remote_terminate_task(task_id, username):
    '''
            终止任务，终止后，任务不可进行任务操作
    @param task_id: 任务id
    @param username: 操作人的用户名
    @return {'result': True/False, 'message':附加信息}
    '''
    try:
        post_resume = {
            "task_id": task_id,
            'username': username,
        }
        resp = http_request_workbench(URL_TERMINATE_TASK, 'POST', post_resume)
        return {'result': resp['result'], 'message': resp['message']}
    except Exception as e:
        logger.error(u"调用蓝鲸远程服务失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用蓝鲸远程服务失败，错误信息:%s" % e}
