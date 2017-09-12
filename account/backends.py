# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from account.factories import AccountFactory
from common.log import logger


class TicketBackend(ModelBackend):
    """
    后台验证
    """
    def authenticate(self, ticket=None, request=None, user_info=None):
        if not user_info:
            account = AccountFactory.getAccountObj()
            status, user = account.check_backend_login_status(request)
        else:
            # 检查此用户是否在django用户表里
            status = True
            userName = user_info.get("username", "")
            user_model = get_user_model()
            try:
                user = user_model.objects.get(username=userName)
            except user_model.DoesNotExist:
                # 第一次登录的时候要新建一个user
                user = user_model(username=userName)
                user.save()
            setattr(user, 'full_info', user_info)

        if not status or not user:
            return None

        return user


class WXBackend(ModelBackend):
    """
    通过统一登录接口进行用户微信认证的 Backend.
    """
    def authenticate(self, request=None, user_info=None):
        try:
            if not user_info or not user_info.get('username', ''):
                return None
            userName = user_info.get('username', '')
            user_model = get_user_model()
            try:
                user = user_model.objects.get(username=userName)
            except user_model.DoesNotExist:
                # 第一次登录的时候要新建一个user
                user = user_model(username=userName)
                user.save()
        except Exception as error:
            logger.error(u"微信验证异常: %s" % error)
            user = None
        return user
