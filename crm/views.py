from django.shortcuts import render, HttpResponse, redirect
from crm import models
from crm.used_forms import own_forms
from django.db import IntegrityError
import string, random
from django.core.cache import cache
import os
from PerfectCRM import settings


# Create your views here.

def sales_index(req):
    return render(req, 'index_content.html')


# def sales(req):
#     return render(req, 'crm/sales/sales.html')

# def customers(req):
#     return render(req,'crm/customers/customers.html')
#



def enrollment(req, row_id):
    msgs = {}
    customer = models.Customer.objects.get(id=row_id)
    if req.method == "POST":
        enrollment_form = own_forms.EnrollmentForm(req.POST)
        if enrollment_form.is_valid():
            msg = '''请将此链接发送给客户进行填写：
                           http://www.caicai.com:8000/crm/register/{enrole_id}/{random_str}/
                           '''

            random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 8))
            try:
                enrollment_form.cleaned_data['customer'] = customer
                enrole_obj = models.Enrollment.objects.create(**enrollment_form.cleaned_data)
                msgs['msg'] = msg.format(enrole_id=enrole_obj.id, random_str=random_str)
                # cache.set(enrole_obj.id, random_str, 20)
            except IntegrityError as e:

                enrole_obj = models.Enrollment.objects.get(customer_id=row_id,
                                                           cls_id=enrollment_form.cleaned_data['cls'].id)
                enrollment_form.add_error('__all__', '该用户此条信息已存在，请勿重复创建！')
                msgs['msg'] = msg.format(enrole_id=enrole_obj.id, random_str=random_str)
            if enrole_obj.contract_agreed:
                return redirect('/crm/contract_review/%s/' % enrole_obj.id)

            cache.set(enrole_obj.id, random_str, 3000)


    else:
        enrollment_form = own_forms.EnrollmentForm()
    return render(req, 'perfect_crm/enrollment.html', {'enrolement': enrollment_form,
                                                       'customer': customer,
                                                       'msgs': msgs})
    pass


def register(req, enroll_id, random_str):
    if cache.get(enroll_id) == random_str:
        status = {}
        enrollment_obj = models.Enrollment.objects.get(id=enroll_id)
        customer_obj_form = own_forms.CustomerForm(instance=enrollment_obj.customer)
        if enrollment_obj.contract_agreed:
            status["status"] = True
        else:
            status["status"] = False
        if req.method == "POST":
            if req.is_ajax():
                enroll_data_dir = os.path.join(settings.ENROLLED_DATA, str(enroll_id))
                if not os.path.exists(enroll_data_dir):
                    os.makedirs(enroll_data_dir, exist_ok=True)
                for k, file in req.FILES.items():
                    with open('%s/%s' % (enroll_data_dir, file.name), 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                return HttpResponse('ok')
            customer_obj_form = own_forms.CustomerForm(req.POST, instance=enrollment_obj.customer)
            if customer_obj_form.is_valid():
                customer_obj_form.save()
                enrollment_obj.contract_agreed = True
                enrollment_obj.save()
                status["status"] = True
                return render(req, "crm/sales/register.html", {'status': status})
        return render(req, "crm/sales/register.html", {'customer_obj_form': customer_obj_form,
                                                       'enrollment_obj': enrollment_obj,
                                                       'status': status,
                                                       })
    else:
        return HttpResponse("去你妈的狗日的！")
    pass


def contract_review(req, enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_form = own_forms.EnrollmentForm(instance=enroll_obj)
    customer_form = own_forms.CustomerForm(instance=enroll_obj.customer)
    # issss = models.Payment.objects.get()
    # print(issss)
    # payment_form = own_forms.PaymentForm()
    return render(req, 'crm/sales/contract_review.html', {
        'enroll_obj': enroll_obj,
        'customer_form': customer_form,
        'enrollment_form': enroll_form,
    })


def enrollment_objection(req, enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_agreed = False
    enroll_obj.save()
    return redirect('/crm/%s/enrollment' % enroll_obj.customer.id)


def payment(req, enroll_id):
    errors = {}
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_approved = True
    enroll_obj.save()
    payment_form = own_forms.PaymentForm()

    if req.method == "POST":
        errors = {}
        payment_amount = req.POST.get("amount", 0)
        # print('dfasfasdfsadfasdf',payment_amount)
        if payment_amount:
            payment_amount = int(payment_amount)
            if payment_amount < 500:
                errors["lower"] = "缴费金额不得少于500元"
            else:
                payment_obj = models.Payment.objects.create(customer=enroll_obj.customer,
                                                            course=enroll_obj.cls.course,
                                                            amount=payment_amount,
                                                            consultant=enroll_obj.consultant
                                                            )
                enroll_obj.customer.status = 1
                enroll_obj.customer.save()
                return redirect('/king_admin/crm/customer/')
        else:
            errors["null"] = "请输入缴费金额"

    return render(req, 'crm/sales/payment.html', {'enroll_obj': enroll_obj,
                                                  'payment_form': payment_form,
                                                  'errors': errors,
                                                  })


def my_class_list(req):
    return render(req, 'crm/sales/my_students.html')