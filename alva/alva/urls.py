from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


import blogs.views as blog_views

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'^$', blog_views.ProfileView.as_view(), name='profile'),

    # Blog CRUD
    url(r'^blog/add/$', blog_views.BlogCreate.as_view(), name='blog_add'),
    url(r'^blog/(?P<pk>\d+)/$', blog_views.BlogUpdate.as_view(), name='blog_update'),
    url(r'^blog/(?P<pk>\d+)/delete/$', blog_views.BlogDelete.as_view(), name='blog_delete'),

    # Post CRUD
    url(r'^post/add/$', blog_views.PostCreate.as_view(), name='post_add'),
    url(r'^post/add/(?P<blog_id>\d+)$', blog_views.PostCreate.as_view(), name='post_add'),
    url(r'^post/(?P<pk>\d+)/$', blog_views.PostUpdate.as_view(), name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete/$', blog_views.PostDelete.as_view(), name='post_delete'),

    # Story CRUD
    url(r'^story/add/(?P<blog_id>\d+)$', blog_views.StoryCreate.as_view(), name='story_add'),
    url(r'^story/(?P<pk>\d+)/$', blog_views.StoryUpdate.as_view(), name='story_update'),
    url(r'^story/(?P<pk>\d+)/delete/$', blog_views.StoryDelete.as_view(), name='story_delete'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Markup renderers
    url(r'^markitup/preview/rest/$', blog_views.rest_preview, name='rest_preview'),
    url(r'^markitup/preview/markdown/$', blog_views.markdown_preview, name='markdown_preview'),
    url(r'^markitup/preview/textile/$', blog_views.textile_preview, name='textile_preview'),
)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),
)
