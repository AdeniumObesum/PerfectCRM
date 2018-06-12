#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : king_admin.py
# @Author: A.O.
# @Date  : 2018/4/27 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django.shortcuts import render, redirect, HttpResponse

from crm import models

enabled_admin = {}


class BaseAdmin(object):
    app_name = ''
    table_name = ''
    list_display = ()
    readonly_fields = ()
    readonly_table = False
    list_filter = ()
    list_per_page = 20
    search_field = ()
    filter_horizontal = ()
    actions = []
    exclude_fields = ()
    model = ''

    def delete_selected(self, req, querysets):
        # print('this is admin:',req,querysets)
        checked_ids = ','.join(str(i.id) for i in querysets)
        errors = {}
        if self.readonly_table:
            errors = {"readonly": "This table is readonly,can`t be delete!"}
        rend = render(req, 'king_admin/table_content_delete.html', {
            "delete_obj": querysets,
            'admin': self,
            'checked_ids': checked_ids,
            'errors':errors,
        })
        return rend

    def default_form_validation(self, my_form):
        '''用户自定义表单验证,相当于clean方法'''
        pass


class CustomerAdmin(BaseAdmin):
    list_display = ('name', 'qq', 'derive', 'status', 'date','enrole')
    list_filter = ('consultant', 'consult_course', 'status', 'date')
    search_field = ('name', 'qq')
    filter_horizontal = ('tags',)
    readonly_fields = ('qq',  'derive','tags')
    list_per_page = 3
    actions = ['test', ]
    readonly_table = False
    def test(self):
        pass

    test.display_name = '测试'

    def enrole(self):
        if self.instance.status == 1:
            return "<a href='/crm/%s/enrollment'>报名新课程</a>"%self.instance.id
        else:
            return "<a href='/crm/%s/enrollment'>报名</a>"%self.instance.id
    enrole.display_name = '报名链接'

    def default_form_validation(self, my_form):
        error_list = []
        # a=my_form.ValidationError('这是一串假的错误提示%(value)s',
        #                         code='invalid',
        #                         params={'value':'(value)'}
        #                         )
        # error_list.append(a)
        return error_list

    def clean_phone(self):
        data = self.cleaned_data.get("phone")
        # print('clean_phone:', self.cleaned_data)
        if not data:
            self.add_error('phone', '不能为空！')
        else:
            return data
        pass

class StudyRecordAdmin(BaseAdmin):
    list_display = ("student", "course_record", "attendance", "score")
    list_filter = ("course_record",)


class CourseRecordAdmin(BaseAdmin):
    list_display = ("cls", "day_num", "teacher", "has_homework", "homework_title", "date",)
    actions = ['initialize_studyrecords',]

    def initialize_studyrecords(self, req, queryset):
        if len(queryset) > 1:
            return HttpResponse("只能选择一个班级！")
        student_list = []
        for enroll_obj in queryset[0].cls.enrollment_set.all():
            student_list.append(
                models.StudyRecord(
                    student=enroll_obj,
                    course_record=queryset[0],
                    attendance=0,
                    score=0,
                )
            )
        try:
            models.StudyRecord.objects.bulk_create(student_list)
        except Exception as e:
            return HttpResponse("初始化失败，请检查是否有相应记录存在！")
        return redirect("/king_admin/crm/studyrecord/?course_record=%s" % queryset[0].id)

    initialize_studyrecords.display_name = "所有学生学习记录初始化"

class UserProfileAdmin(BaseAdmin):
    list_display = ('name', 'email','is_active','is_admin')
    readonly_fields = ('password',)
    filter_horizontal = ('user_permissions','groups',)
    exclude_fields = ('last_login',)

class RoleAdmin(BaseAdmin):
    list_display = ('name', 'menus')

def register(model_class, admin_class=None):
    if admin_class:
        admin_class.app_name = model_class._meta.app_label
        admin_class.table_name = model_class._meta.model_name
    if model_class._meta.app_label not in enabled_admin:
        enabled_admin[model_class._meta.app_label] = {}
    admin_class.model = model_class
    enabled_admin[model_class._meta.app_label][model_class._meta.model_name] = admin_class

register(models.Customer, CustomerAdmin)
register(models.UserProfile, UserProfileAdmin)
register(models.Role, RoleAdmin)
register(models.StudyRecord, StudyRecordAdmin)
register(models.CourseRecord, CourseRecordAdmin)
# print(enabled_admin['crm']['customer'].model)
