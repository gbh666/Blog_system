#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/5

from django.conf.urls import url
from blog import views

urlpatterns = [

    # url(r'^(?P<article_type_id>\d+)/', views.index),
    url(r'poll/', views.poll),
    url(r'comment/', views.comment),
    url(r'upload_file/', views.upload_file),
    url(r'article/delete_article', views.delete_article),
    url("(?P<user_site>\w+)/article/add_article", views.add_article),
    url("(?P<user_site>\w+)/article/back_stage", views.back_stage),
    url("(?P<user_site>\w+)/article/(?P<condition>category|tag|date)/(?P<para>(\d+\-\d+\-\d+)|(\w+))", views.userindex),
    url(r"^(?P<user_site>\w+)/article/(?P<article_nid>\d+)",views.article_content),
    url(r"^(?P<user_site>\w+)/article2/(?P<article_nid>\d+)",views.article_detail2),
    url("(?P<user_site>\w+)/", views.userindex),

]
