#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : own_forms.py
# @Author: A.O.
# @Date  : 2018/5/13 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django.forms import ModelForm
from crm import models

class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        # print(cls.base_fields.items())
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model = models.Enrollment
        fields = ['cls','consultant']

class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field in cls.base_fields.items():
            field.widget.attrs['class']='form-control'
            if field_name in cls.Meta.readonly_fields:
                field.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)

    def clean_qq(self):
        if self.instance.qq != self.cleaned_data['qq']:
            self.add_error('QQ','臭傻逼，你干啥！')
        else:
            return self.cleaned_data['qq']
    class Meta:
        model= models.Customer
        fields = '__all__'
        exclude = ['content','tags','remark','status','referral_from','consult_course']
        readonly_fields = ['qq','consultant','derive']


class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field in cls.base_fields.items():
            field.widget.attrs['class']='form-control'
        return ModelForm.__new__(cls)


    class Meta:
        model = models.Payment
        fields = '__all__'