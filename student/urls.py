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
    path('',views.my_course,name='stu_course'),
    path('studyrecords/<enroll_obj_id>/',views.studyrecords,name='studyrecords'),
    path('homework_detail/<study_record_id>/',views.homework_detail,name='homework_detail'),

]
