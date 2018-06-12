from django.shortcuts import render, redirect, HttpResponse
from king_admin import king_admin
import importlib
from king_admin import utils
import json
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from king_admin import my_forms
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def acc_login(req):
    errors = {}
    if req.method == 'POST':

        _email = req.POST.get('email')
        _password = req.POST.get('password')
        user = authenticate(username=_email,password=_password)
        if user:

            login(req,user)
            next_url = req.GET.get('next','/')
            return redirect(next_url)
        else:
            errors["error"] = "邮箱或密码错误！"
        print(user,errors)
    return render(req,"perfect_crm/acc_login.html",{"errors":errors})


def acc_logout(req):
    logout(req)
    return redirect('/acc_login/')
    pass

def index(req):

    return render(req, 'index_content.html')



def test(req):

    return render(req,'perfect_crm/test.html')
    pass