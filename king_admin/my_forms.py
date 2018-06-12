#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : my_forms.py
# @Author: A.O.
# @Date  : 2018/5/3 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django.utils.translation import ugettext as _
from django.forms import ModelForm, forms, ValidationError
from crm import models


def create_model_form(req, admin,add_form=False):
    def __new__(cls, *args, **kwargs):
        # print(cls.base_fields.items())
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            # v.widget.attrs['maxlength']=getattr(v,'max_length') if hasattr(v,'max_length') else '32'
            # v.widget.attrs['width']=getattr(v,'max_length') if hasattr(v,'max_length') else '32' ##因为form-control宽度是100%，设置不生效
            if not add_form:
                if field_name in admin.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

            if hasattr(admin, 'clean_%s' % field_name):
                clean_field_func = getattr(admin, 'clean_%s' % field_name)
                setattr(cls, "clean_%s" % field_name, clean_field_func)

        return ModelForm.__new__(cls)

    def default_clean(self):
        '''给所有的form加一个clean验证'''
        error_list = []
        if self.instance.id:
            for field in admin.readonly_fields:
                field_val = getattr(self.instance, field)
                field_val_from_web = self.cleaned_data.get(field)
                if hasattr(field_val, "select_related"):  # 代表是多对多关系，得到的field_val 是一个对象
                    m2m_query = field_val.select_related()
                    field_val = set(m2m_query)
                    field_val_from_web = set(field_val_from_web)
                    # print(m2m_query,field_val_from_web,m2m_query == field_val_from_web)
                    # if field_val == field_val_from_web:
                    #     # print("相等")
                    #     continue

                if field_val != field_val_from_web:
                    error_list.append(ValidationError(_(
                        'Field %(field)s is readonly,data should be %(value)s '),
                        code='invalid',
                        params={'field': field, 'value': field_val},
                    ))

        self.ValidationError = ValidationError
        response = admin.default_form_validation(admin, self)
        if admin.readonly_table:
            error_list.append(ValidationError(_(
                'Table is readonly ! '),
                code='invalid',
                params={},
            ))
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)

            # clean_data = self.cleaned_data
            # print('ooooooooooooooocleanoooooooooooooo')
            # print(admin.readonly_fields)
            # print(self.instance.phone)
            # print(clean_data)

    class meta:
        model = admin.model
        fields = "__all__"
        exclude = admin.exclude_fields
    attr = {"Meta": meta, "__new__": __new__, "clean": default_clean}

    _model_form_clss = type('DynamicModelForm', (ModelForm,), attr)
    # setattr(_model_form_clss,'Meta',meta)


    return _model_form_clss

    pass
