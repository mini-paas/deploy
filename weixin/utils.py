# -*- coding: utf-8 -*-
from settings import RUN_MODE, WEIXIN_BK_URL, SITE_URL


def is_weixin_visit(request):
    """
    是否微信端登录
    """
    WEIXIN_URL_PREFIX = '%sweixin/' % SITE_URL
    request_origin_url = "http://%s" % request.get_host()
    if RUN_MODE != 'DEVELOP' and request.path.startswith(WEIXIN_URL_PREFIX) and request_origin_url == WEIXIN_BK_URL:
        return True
    return False
