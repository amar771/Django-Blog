from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^.*index.*$', views.index, name='index'),
    url(r'^post/(?P<slug>[\w-]+)/$', views.post_detail, name='post_detail'),
    url(r'^new/post$', views.post_new, name='post_new'),
    url(r'^new/post/$', views.post_new, name='post_new'),
    url(r'^post/(?P<slug>[\w-]+)/edit/#', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<slug>[\w-]+)/publish/$', views.post_publish,
        name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove,
        name='post_remove'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove,
        name='comment_remove'),
    url(r'^comment/(?P<pk>\d+)', views.comment_undelete,
        name='comment_undelete'),
    url(r'^deleted/$', views.deleted, name='deleted'),
    url(r'^about$', views.about, name='about'),
    url(r'^about/new$', views.about_new, name='about_new'),
    url(r'^about/(?P<pk>\d+)/edit$', views.about_edit, name='about_edit'),
    url(r'^contact$', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
