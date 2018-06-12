#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: A.O.
# @Date  : 2018/4/29 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django.db.models import Q
def table_filter(req,admin):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    key_words = ['page','o','_q']

    for k, v in req.GET.items():
        if k not in key_words:##分页关键字和排序关键字和查找关键字
            if v:
                if type(admin.model._meta.get_field(k)).__name__ in ['DateTimeField','DateField']:
                    filter_conditions[k+'__gte'] = v
                else:
                    filter_conditions[k] = v


    # print(filter_conditions)
    # print(admin.model.objects.filter(**filter_conditions))
    return admin.model.objects.filter(**filter_conditions).order_by('-id'), filter_conditions


def table_sort(req,admin,content_set):
    '''数据排序'''
    order_by = req.GET.get('o','')
    if hasattr(admin.model,order_by):
        if order_by:
            res = content_set.order_by(order_by)
            if order_by.startswith('-'):
                order_by = order_by.strip('-')
            else:
                order_by = "-%s"%order_by

            return res,order_by
    return content_set,order_by

def search_for(req,content_set,admin):
    search_key = req.GET.get('_q','')
    q_obj = Q()
    q_obj.connector = 'OR'
    for column in admin.search_field:
        q_obj.children.append(('%s__contains'%column,search_key))

    res = content_set.filter(q_obj)
    return res,search_key
    pass