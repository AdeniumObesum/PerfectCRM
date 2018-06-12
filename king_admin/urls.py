#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: A.O.
# @Date  : 2018/4/24 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',views.index),
    path('', views.index, name='table_index'),
    path('<app_name>/<table_name>/', views.table_contents, name='table_contents'),
    path('<app_name>/<table_name>/<row_id>/change/', views.table_content_change, name='table_content_change'),
    path('<app_name>/<table_name>/<row_id>/change/password/', views.password_reset, name='password_reset'),
    path('<app_name>/<table_name>/<row_id>/delete/', views.table_content_delete, name='table_content_delete'),
    path('<app_name>/<table_name>/add/', views.table_content_add, name='table_content_add'),
    path('<app_name>/<table_name>/checked_list/handle/',views.checked_list_handle,name='checked_list_handle'),
    path('test',views.test),
]
