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
    url(r'^post/add/(?P<blog_id>\d+)$', blog_views.PostCreate.as_view(), name='post_add'),
    url(r'^post/(?P<pk>\d+)/$', blog_views.PostUpdate.as_view(), name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete/$', blog_views.PostDelete.as_view(), name='post_delete'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),
)
