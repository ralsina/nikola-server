from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


import blogs.views as blog_views

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'^$', blog_views.ProfileView.as_view(), name='profile'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),
)
