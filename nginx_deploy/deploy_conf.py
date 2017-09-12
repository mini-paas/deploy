# coding=utf-8

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


def get_object(model, **kwargs):

    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def page_list_return(total, current=1):
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):

    paginator = Paginator(post_objects, 15)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end


def my_render(template, data, request):

    return render_to_response(template, data, context_instance=RequestContext(request))


class ServerError(Exception):
    pass