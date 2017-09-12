# -*- coding: utf-8 -*-
from common.log import logger
from app_control.models import Function_controller


def func_check(func_code):
    """
    @summary: 检查功能是否开放
    @param func_code 功能ID
    @return (0/1/2/3, message)
            #如下 (0, No check)
                  (1, check success)
                  (2, check failed)
                  (3, error_message)
    """
    result = Function_controller.objects.func_check(func_code)
    if result['result']:
        if result['message']:
            return (1, 'check success')
        else:
            return (2, 'check failed')
    else:
        logger.error(u"check error,%s" % result['message'])
        return (3, 'check error,%s' % result['message'])
