#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tags.py
# @Author: A.O.
# @Date  : 2018/4/28 
# @license : Copyright(C), Nanyang Institute of Technology 
# @Contact : 1837866781@qq.com 
# @Software : PyCharm
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
from django.core.exceptions import FieldDoesNotExist
register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_contents_all(admin):
    content_set = admin.model.objects.all()
    return content_set


@register.simple_tag
def contents_show(obj, admin):
    row_element = ""

    for index, column in enumerate(admin.list_display):

        try:
            field_content = obj._meta.get_field(column)

            if field_content.choices:
                column_data = getattr(obj, "get_%s_display" % column)()
            else:
                column_data = getattr(obj, column)
        except FieldDoesNotExist as e:
            if hasattr(admin,column):
                column_data_func = getattr(admin,column)
                admin.instance = obj
                column_data = column_data_func()
        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if index == 0:
            row_element += """<td><a href="%s/change/">%s</a></td>""" % (obj.id, column_data)
        else:
            row_element += "<td>%s</td>" % column_data
    return mark_safe(row_element)


@register.simple_tag
def get_url_append(filter_conditions):
    filters = ''
    for k, v in filter_conditions.items():
        if '__gte' in k:
            k = k[0:-5]
        filters += '%s=%s&' % (k, v)
    # filters+='o=%s'%order_by
    return filters


@register.simple_tag
def render_page_ele(loop_counter, content_set, filter_conditions, conf):
    # filters = ''
    # for k,v in  filter_conditions.items():
    #     filters += '%s=%s&'%(k,v)
    filters = get_url_append(filter_conditions)
    ele_class = ""
    if content_set.number == loop_counter:
        ele_class = "active"
    if loop_counter <= content_set.number:
        if loop_counter <= 3 or content_set.number - 4 < loop_counter:
            if loop_counter == 3 and content_set.number > 6:
                ele = '''<li><span>...</span></li>'''
            else:
                ele = '''<li class="%s"><a href="?%spage=%s&o=%s&_q=%s">%s</a></li>''' % (
                    ele_class, filters, loop_counter, conf["old_order_by"], conf["search_key"], loop_counter)
            return mark_safe(ele)
    elif loop_counter > content_set.number:
        if loop_counter > content_set.paginator.num_pages - 3 or loop_counter < content_set.number + 4:
            if loop_counter == content_set.paginator.num_pages - 2 and content_set.paginator.num_pages - content_set.number > 5:
                ele = '''<li><span>...</span></li>'''
            else:
                ele = '''<li class="%s"><a href="?%spage=%s&o=%s&_q=%s">%s</a></li>''' % (
                    ele_class, filters, loop_counter, conf["old_order_by"], conf["search_key"], loop_counter)
            return mark_safe(ele)
    return ''


@register.simple_tag
def handle_order_by(column, order_by):
    if order_by:
        if order_by.strip('-') == column:
            # print('-' in order_by)
            return order_by
        else:
            return column
    return column


@register.simple_tag
def render_filter_ele(condition, admin_class, filter_conditions):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' % condition
    field_obj = admin_class.model._meta.get_field(condition)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:

            # print(filter_conditions.get(condition))
            # print("choice",choice_item,filter_conditions.get(condition),type(filter_conditions.get(condition)))
            if filter_conditions.get(condition) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            # print(choice_item)
            # print('111',field_obj,)
            if filter_conditions.get(condition) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        selected = ''
        date_today = datetime.now()
        date_ele = [('今天', date_today.date()),
                    ('昨天', date_today.date() - timedelta(days=1)),
                    ('近七天', date_today.date() - timedelta(days=7)),
                    ('本月', date_today.date().replace(day=1)),
                    ('近一个月', date_today.date() - timedelta(days=30)),
                    ('近三个月', date_today.date() - timedelta(days=90)),
                    ('近半年', date_today.date() - timedelta(days=180)),
                    ('本年', date_today.date().replace(month=1)),
                    ('近一年', date_today.date() - timedelta(days=365)),
                    ]
        for op in date_ele:
            select_ele += '''<option value='%s' %s>%s</option>''' % (op[1], selected, op[0])

        pass
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def select_has_choosed_box_option(admin, field, row_id, form_obj):
    tags_field = admin.model._meta.get_field(field.name)
    row_option = ''
    if row_id:
        field_obj = getattr(form_obj.instance, field.name)
        query_set = field_obj.all()
        for row in query_set:
            row_option += '<option value=%s>%s</option>' % (row.id, row)
    else:
        pass
    return mark_safe(row_option)


pass


@register.simple_tag
def select_not_choosed_box_option(admin, field, row_id, form_obj):
    tags_field = admin.model._meta.get_field(field.name)
    all_tags = tags_field.related_model.objects.all()

    row_option = ''
    exclude_id = []
    if row_id:  # 获取没有选中的值的id
        some_tags = getattr(form_obj.instance, field.name).all()
        for tag in some_tags:
            if tag in all_tags:
                exclude_id.append(tag.id)

        all_tags = tags_field.related_model.objects.exclude(id__in=exclude_id).all()

        for row in all_tags:
            row_option += '<option value=%s>%s</option>' % (row.id, row)
    else:  # 返回空
        query_set = tags_field.related_model.objects.all()
        for row in query_set:
            row_option += '<option value=%s>%s</option>' % (row.id, row)

    return mark_safe(row_option)

    pass


@register.simple_tag
def display_obj_related(objs):
    '''取出关联数据'''
    if type(objs).__name__ == 'QuerySet':
        # for obj in objs:
        #     print(type(obj))
        #     new_objs.append(obj)
        new_objs = objs
    else:
        new_objs = [objs, ]
    if new_objs:
        # model_class = objs[0]._meta.model
        # model_name = objs[0]._meta.model_name
        # print(new_objs)

        related_ele = related_ele_show(new_objs)
        return mark_safe(related_ele)
    pass


def related_ele_show(objs):
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li>%s: %s</li>''' % (obj._meta.verbose_name, obj.__str__())
        ul_ele += li_ele
        if hasattr(obj._meta, 'local_many_to_many'):  ###tags显示
            sub_ul = '<ul>'
            for m2m_field in obj._meta.local_many_to_many:
                m2m_field_obj = getattr(obj, m2m_field.name)
                for no_name in m2m_field_obj.select_related():
                    li_ele = '''<li>%s: %s</li>''' % (m2m_field.verbose_name, no_name.__str__())
                    sub_ul += li_ele
                sub_ul += '</ul>'
            ul_ele += sub_ul
        for related_obj in obj._meta.related_objects:
            # print(related_obj.__repr__())
            if 'ManyToManyRel' in related_obj.__repr__():
                if hasattr(obj, related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    if hasattr(accessor_obj, 'select_related'):
                        target_objs = accessor_obj.model.objects.all()
                        sub_ul = "<ul style='color:red'>"
                        for i in target_objs:
                            li_ele = '''<li>%s: %s</li>''' % (i._meta.verbose_name, i.__str__())
                            sub_ul += li_ele
                        sub_ul += "</ul>"
                        ul_ele += sub_ul
                        # print(sub_ul)
            elif hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                if hasattr(accessor_obj, 'select_related'):
                    target_objs = accessor_obj.select_related()
                else:
                    target_objs = accessor_obj
                if len(target_objs) > 0:
                    node = related_ele_show(target_objs)
                    ul_ele += node
    ul_ele += "</ul>"
    return ul_ele
    pass


@register.simple_tag
def show_action_name(admin,action):
    if hasattr(admin,action):
        func=getattr(admin,action)
        return func.display_name if hasattr(func,"display_name") else action
    pass

@register.simple_tag
def get_column_verbose_name(admin,column):
    if hasattr(admin.model,column):
        column = admin.model._meta.get_field(column).verbose_name
    if hasattr(admin,column):
       column = getattr(admin,column).display_name
    column = column.upper()
    return column