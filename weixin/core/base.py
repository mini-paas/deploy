# -*- coding: utf-8 -*-
import abc
import random
import string
import time
import hmac
import base64
import hashlib

import requests

import settings
from common.log import logger


class API(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        try:
            curModule = __import__('weixin.core', globals(), {}, ['settings_weixin_api'])
            self._config = curModule.settings_weixin_api
        except Exception, e:
            self._config = None
            logger.error(u"加载settings_weixin_api 配置文件出错：%s" % e)
        self.app_code = settings.APP_CODE
        self.secret_key = settings.SECRET_KEY
        self.timeout = 10
        self.ssl_verify = False

    def http_get(self, _http_url, **kwargs):
        """
        http 请求GET方法
        """
        try:
            resp = requests.get(_http_url, params=kwargs, timeout=self.timeout, verify=self.ssl_verify)
            resp = resp.json()
            return resp
        except Exception as error:
            logger.error('requests get url:%s error: %s' % (_http_url, error))
            return {}

    def http_post(self, _http_url, **kwargs):
        """
        http 请求POST方法
        """
        try:
            resp = requests.post(_http_url, json=kwargs, timeout=self.timeout, verify=self.ssl_verify)
            resp = resp.json()
            return resp
        except Exception as error:
            logger.error('requests post url:%s kwargs: %s error %s' % (_http_url, kwargs, error))
            return {}

    def nonce_str(self, length=15):
        """
        随机字符串
        """
        nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        return nonce

    def nonce_num(self, upper_limit_length=6):
        """
        指定位数的随机数
        upper_limit_length: 上限位数
        """
        if upper_limit_length > 0 and upper_limit_length <= 1000:
            end_num = 10 ** (upper_limit_length + 1) - 1
            num = random.randint(1, end_num)
        else:
            num = 1
        return num

    def gen_signature(self, query_param, url_path, request_method):
        """
        生成签名
        """
        params = '&'.join(['%s=%s' % (key, query_param[key]) for key in sorted(query_param)])
        message = '%s%s?%s' % (request_method, url_path, params)
        digest_make = hmac.new(self.secret_key, message, hashlib.sha1).digest()
        _signature = base64.b64encode(digest_make)
        return _signature

    @property
    def timestamp(self):
        """
        时间戳
        """
        return int(time.time())
