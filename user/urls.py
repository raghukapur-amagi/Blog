
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^_login/$', views.login_user, name='login_user'),
    url(r'^_logout/$', views.logout_user, name='logout_user'),
    url(r'^_register/$', views.register_user, name='register_user'),
    url('register', views.register, name='register'),
    url('login', views.login_request, name='login'),
    url('logout', views.logout_request, name='logout'),
    url('home', views.homepage, name='homepage'),
]
