from django.shortcuts import render, redirect, HttpResponse
from king_admin import king_admin
import importlib
from king_admin import utils
import json
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from king_admin import my_forms
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(req):
    return render(req, 'king_admin/index.html', {"table_dic": king_admin.enabled_admin})

@login_required
def table_contents(req, app_name, table_name):
    conf = {}
    table_admin = king_admin.enabled_admin[app_name][table_name]
    object_list, filter_conditions = utils.table_filter(req, table_admin)  ##过滤后的结果

    object_list, search_key = utils.search_for(req, object_list, table_admin)

    object_list, order_by = utils.table_sort(req, table_admin, object_list)  ##排序后的结果

    old_order_by = req.GET.get('o', '')  # 记录当前排序状态
    conf['order_by'] = order_by  ##加负号或者去掉负号的过滤值
    conf['old_order_by'] = old_order_by  ###上一次的过滤值
    conf['app'] = app_name
    conf['table'] = table_name
    conf['search_key'] = search_key  ##搜索框保留值
    # conf['current_url'] = req.path
    # print(req.path)

    paginator = Paginator(object_list, table_admin.list_per_page)
    page = req.GET.get('page')
    try:
        content_set = paginator.page(page)
    except PageNotAnInteger:
        content_set = paginator.page(1)
    except EmptyPage:
        content_set = paginator.page(paginator.num_pages)
    return render(req, 'king_admin/table_contents.html',
                  {'admin': table_admin,
                   'content_set': content_set,
                   'filter_conditions': filter_conditions,
                   'conf': conf,
                   },
                  )


@login_required
def table_content_change(req, app_name, table_name, row_id):
    conf = {}
    conf["row_id"] = row_id
    conf['app'] = app_name
    conf['table'] = table_name
    table_admin = king_admin.enabled_admin[app_name][table_name]
    model_form_class = my_forms.create_model_form(req, table_admin)
    isinstance_obj = table_admin.model.objects.get(id=row_id)
    errors = {}


    if req.method == "POST" :
        form_obj = model_form_class(req.POST, instance=isinstance_obj)
        if not table_admin.readonly_table:
            if form_obj.is_valid():
                form_obj.save()
                return redirect('/king_admin/%s/%s/' % (app_name, table_name))
    else:
        form_obj = model_form_class(instance=isinstance_obj)
        errors = {"readonly": "This table is readonly,can`t be delete!"}
    return render(req, 'king_admin/table_content_change.html', {'form_obj': form_obj, 'admin': table_admin,
                                                                'conf': conf,
                                                                'errors':errors
                                                                })

@login_required
def table_content_add(req, app_name, table_name):
    conf = {}
    conf["row_id"] = None
    conf["add_form"] = True
    table_admin = king_admin.enabled_admin[app_name][table_name]
    table_admin.is_add_form= True
    model_form_class = my_forms.create_model_form(req, table_admin,add_form=True)


    if req.method == "POST" :
        form_obj = model_form_class(req.POST)
        if not table_admin.readonly_table:
            if form_obj.is_valid():
                form_obj.save()
                # return redirect('/king_admin/%s/%s/'%(app_name,table_name))
                return redirect(req.path.replace('/add/', '/'))
    else:
        form_obj = model_form_class()

    return render(req, 'king_admin/table_content_add.html',
                  {'form_obj': form_obj,
                   'admin': table_admin,
                   'conf': conf,
                   })

@login_required
def table_content_delete(req, app_name, table_name, row_id):
    conf = {}
    table_admin = king_admin.enabled_admin[app_name][table_name]
    delete_ing_obj = table_admin.model.objects.get(id=row_id)

    errors = {}
    if req.method == "POST":
        if not table_admin.readonly_table:
            delete_ing_obj.delete()
            return redirect('/king_admin/%s/%s/' % (app_name, table_name))
        else:
            return redirect('/king_admin/%s/%s/' % (app_name, table_name))
    if table_admin.readonly_table:
        errors = {"readonly":"This table is readonly,can`t be delete!"}
    return render(req, 'king_admin/table_content_delete.html', {
        'delete_obj': delete_ing_obj,
        'admin': table_admin,
        'errors':errors,
    })

@login_required
def checked_list_handle(req, app_name, table_name):
    table_admin = king_admin.enabled_admin[app_name][table_name]
    if req.method == "POST":
        if 'delete_confirm' not in req.POST:
            checked_list = req.POST.getlist("checked_list",'')
            action = req.POST.get("actions",'')
            try:
                query_sets = table_admin.model.objects.filter(id__in=checked_list)
                # print('this is view:',query_sets)
                if not query_sets:
                    return HttpResponse("未选中任何人！")
            except:
                return HttpResponse("值获取失败！")

            if hasattr(table_admin, action):
                func_action = getattr(table_admin, action)
                return func_action(table_admin, req, query_sets)

                # print(checked_list,':',type(checked_list))
                # print(action,':',type(action))
        else:
            if not table_admin.readonly_table:
                str_ids = req.POST.get("checked_ids",'')
                checked_ids = str_ids.split(',')
                query_sets = table_admin.model.objects.filter(id__in=checked_ids)
                query_sets.delete()
            else:
                return redirect('/king_admin/%s/%s/' % (app_name, table_name))
    return redirect('/king_admin/%s/%s/' % (app_name, table_name))

    pass

@login_required
def password_reset(req,app_name,table_name,row_id):
    conf = {}
    error = {}
    table_admin = king_admin.enabled_admin[app_name][table_name]
    change_obj = table_admin.model.objects.get(id=row_id)
    if req.method == 'GET':
      pass
    elif req.method == 'POST':
        _password1 = req.POST.get('password1')
        _password2 = req.POST.get('password2')

        if _password1:
            if _password1 == _password2:

                if len(_password1)>5:
                    change_obj.set_password(_password1)
                    change_obj.save()

                    return redirect(req.path.rstrip("password/"))
                else:
                    error = {"too_short": "密码长度需在6位以上！"}
            else:
                error = {"invalid":"两次密码不一致！"}
        else:
            error = {"not_null": "密码不能为空！"}



    return render(req,"king_admin/password_reset.html",{'change_obj':change_obj,
                                                        'error':error})
    pass


def test(req):

    return render(req,"base.html")