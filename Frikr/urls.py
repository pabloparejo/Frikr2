"""Frikr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from Frikr import settings

from photos import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^photos/$', views.PhotoListView.as_view(), name="photos"),
    url(r'^photos/(?P<pk>[0-9]+)/$', views.PhotoDetailView.as_view(), name="photo_detail"),
    url(r'^photos/(?P<pk>[0-9]+)/(?P<vote>(1|-1))$', views.VoteView.as_view(), name="vote"),
    url(r'^search/$', views.SearchView.as_view(), name="search"),
    url(r'^delete_photo/(?P<pk>[0-9]+)/$', views.PhotoDeleteView.as_view(), name="delete_photo"),
    url(r'^photos/new_photo/$', views.NewPhotoView.as_view(), name="new_photo"),
    url(r'^users/', include('users.urls')),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
                    {'document_root':settings.MEDIA_ROOT}),
]