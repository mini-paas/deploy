# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from common.log import logger

from notice.utils_push import _get_all_notice, _get_user_notread_notice


def notice_home(request):
    """
    通知中心首页
    """
    try:
        username = request.user.username
        notices = []
        # 开启后使用
        all_notice = _get_all_notice()
        unread_num, unread_list = _get_user_notread_notice(username)
        unread_nid_list = [n.get('id') for n in unread_list]
        for n in all_notice:
            if n.get('id') in unread_nid_list:
                n['is_read'] = False
            else:
                n['is_read'] = True
            notices.append(n)
    except Exception, e:
        logger.error(u"通知中心异常：%s" % e)
        notices = []
    result = {'notices': notices}
    return render_mako_context(request, 'notice/notice.html', result)
