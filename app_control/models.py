# -*- coding: utf-8 -*-
import datetime

from django.db import models

from common.log import logger


class Function_Manager(models.Manager):

    def func_check(self, func_code):
        '''
        check func_code是否对外开放
        '''
        try:
            func = self.get(func_code=func_code)
            return {'result': True, 'message': func.enabled}
        except Exception, e:
            logger.error(e)
            return {'result': False, 'message': e}


class Function_controller(models.Model):
    """
    功能开启控制器
    """
    func_code = models.CharField(u"功能code", max_length=64, unique=True)
    func_name = models.CharField(u"功能名称", max_length=64)
    enabled = models.BooleanField(u"是否开启该功能", help_text=u"控制功能是否对外开放，若选择，则该功能将对外开放", default=False)
    create_time = models.DateTimeField(u"创建时间", default=datetime.datetime.now)
    func_developer = models.TextField(u"功能开发者", help_text=u"多个开发者以分号分隔", null=True, blank=True)
    objects = Function_Manager()

    def __unicode__(self):
        return self.func_name

    class Meta:
        app_label = 'app_control'
        verbose_name = u"功能控制器"
        verbose_name_plural = u"功能控制器"
