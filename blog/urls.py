from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^article/(?P<slug>[-\w]+)/$', views.view, name='view'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.update, name='update'),
    url(r'^update/(?P<slug>[-\w]+)/save/$', views.save, name= 'save'),
    url(r'^search/', views.search, name= 'search'),
    url(r'^article/(?P<slug>[-\w]+)/comment/$', views.comment, name='comment'),

]
