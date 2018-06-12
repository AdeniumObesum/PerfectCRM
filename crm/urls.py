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
from crm import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',views.index),
    path('', views.sales_index, name='index'),
    path('<row_id>/enrollment/', views.enrollment, name='enrollment'),
    path('register/<enroll_id>/<random_str>/', views.register, name='register'),
    path('contract_review/<enroll_id>/', views.contract_review, name='contract_review'),
    path('payment/<enroll_id>/', views.payment, name='payment'),
    path('my_class_list/', views.my_class_list, name='my_class_list'),
    path('enrollment_objection/<enroll_id>/', views.enrollment_objection, name='enrollment_objection'),
    # path('sales/', views.sales, name='sales_index'),
    # path('customers/', views.customers, name='customers_index'),

]
