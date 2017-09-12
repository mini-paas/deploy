# -*- coding: utf-8 -*-
from weixin.core.base import API


class WeiXinApi(API):

    def __init__(self):
        super(WeiXinApi, self).__init__()

    # 主要用于微信JS-SDK，(具体使用：http://qydev.weixin.qq.com/wiki/index.php?title=%E5%BE%AE%E4%BF%A1JS-SDK%E6%8E%A5%E5%8F%A3)
    def get_js_sign(self, url, request_method='GET'):
        """
        获取微信JS签名信息
        url: 需要在页面上使用js签名对应的页面url, 一般直接request.build_absolute_uri()可以获取到
        request_method：请求的方式（GET, POST）一般直接request.method 可以获取到
        return:{'result': , 'message': , 'data': {'appId': , 'nonceStr': ,'signature': , 'timestamp': , 'url': }}
        """
        query_param = {
            'app_code': self.app_code,
            'Nonce': self.nonce_num(6),
            'Timestamp': self.timestamp,
            'url': url
        }
        signature = self.gen_signature(query_param, self._config.WEIXIN_GET_JS_SIGN_PATH, request_method)
        query_param['Signature'] = signature
        data = self.http_get(self._config.WEIXIN_GET_JS_SIGN_URL, **query_param)
        return data
