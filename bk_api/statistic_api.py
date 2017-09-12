# -*- coding: utf-8 -*-
"""
@author: sundytian
@date: 2014-02-26
@summary: 统计api
"""
from bk_api.settings_bk import BK_URL, logger
from bk_api.utils import http_request_workbench


# ===============================================================================
# #POST请求
URL_APP_GAINS = '%s/app_api/app_gains_record/' % BK_URL
# ===============================================================================


def remote_app_gains_record(app_code, feature_code, operater, is_task, cc_biz_id=''):
    '''
    app收益统计接口

    @param app_code：app编码
    @param feature_code：app对应功能编码
    @param operater：操作人英文id
    @param is_task：是否为执行任务（0:否，1：是）
    @param cc_biz_id(可选)：cc业务id
    '''
    try:
        post_param = {
            "app_code": app_code,
            'feature_code': feature_code,
            'operater': operater,
            'is_task': is_task,
            'cc_biz_id': cc_biz_id
        }
        resp = http_request_workbench(URL_APP_GAINS, 'POST', post_param)
        return resp
    except Exception as e:
        logger.error(u"调用收益统计接口失败，错误信息:%s" % e)
        return {'result': False, 'message': u"调用收益统计接口失败，错误信息:%s" % e}
