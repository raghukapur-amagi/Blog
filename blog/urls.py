from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^article/(\d+)/$', views.view, name='view'),
    url(r'^update/(\d+)/$', views.update, name='update'),
    url(r'^update/(\d+)/save/', views.save, name= 'save'),
    url(r'^search/', views.search, name= 'search'),
]
