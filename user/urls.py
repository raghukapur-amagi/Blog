
from django.contrib import admin
from django.conf.urls import url
from . import views 


urlpatterns = [
    url('register', views.register, name='register'),
    url('login', views.login_request, name='login'),
    url('logout', views.logout_request, name='logout'),
    url('home', views.homepage, name='homepage'),
    #url('', views.homepage, name='homepage'),
]
