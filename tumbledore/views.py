from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from tumbledore.models import *


def index(request, mount_point):
    page = int(request.GET.get('page', '1'))
    tumblelog = get_object_or_404(Tumblelog, mount_on=mount_point)
    queryset = tumblelog.posts.all() if request.user.is_staff else tumblelog.posts.published()
    object_list = Paginator(queryset, tumblelog.posts_per_page).page(int(page))

    return render(request, '%s/index.html' % tumblelog.theme, {
        'tumblelog': tumblelog,
        'object_list': object_list,
        'widgets': _get_widgets_for(tumblelog),
        })


def post(request, mount_point, slug):
    tumblelog = get_object_or_404(Tumblelog, mount_on=mount_point)
    query_args = {
        'slug': slug,
        'tumblelog_id': tumblelog.id,
        'is_published': True,
        }
    if 'preview' in request.GET.keys():
        del query_args['is_published']
    print query_args
    try:
        post = TumblelogPost.objects.filter(**query_args)[0]
    except IndexError:
        raise Http404

    return render(request, '%s/post.html' % tumblelog.theme, {
        'tumblelog': tumblelog,
        'post': post,
        'widgets': _get_widgets_for(tumblelog),
        })


def widget(request, widget_id):
    widget = get_object_or_404(TumblelogWidget, pk=widget_id)

    return HttpResponse(widget.as_javascript, content_type="text/javascript")


def _get_widgets_for(tumblelog):
    return [placement.widget for placement in tumblelog.placement_set.all()]