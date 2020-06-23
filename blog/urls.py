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
    url(r'^articles/$', views.get_articles, name='get_articels'),
    url(r'^articles/(\d+)/$', views.get_article_detail, name='get_article_detail'),
    url(r'^tags/$', views.get_tags, name='get_tags'),
    url(r'^tags/(\d+)/$', views.get_tag_detail, name='get_tag_detail'),
    url(r'^comments/$', views.get_comments, name='get_comments'),
    url(r'^comments/(\d+)/$', views.get_comment_detail, name='get_comment_detail')

]
