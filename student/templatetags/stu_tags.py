#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stu_tags.py
# @Author: A.O.
# @Date  : 2018/5/18 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Sum
register = template.Library()



@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_records = enroll_obj.studyrecord_set.all().filter(course_record__cls_id=enroll_obj.cls.id)
    # for i in study_records:
    #     print(i)
    return study_records.aggregate(Sum('score'))
    # print(study_records.aggregate(Sum('score')))