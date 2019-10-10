from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.urls import reverse

from common.func import checkNum
from content.models import LunBoTu, ReMaiTu
from user.models import Users


def index(request):
    lunbo = LunBoTu.objects.all()
    remai = ReMaiTu.objects.all()
    user = ''
    login = False
    num = 0
    if request.session.get('phone'):
        phone = request.session.get('phone')
        user = Users.objects.get(phone=phone)
        login = True
        num = checkNum(phone)

    context = {
        'user': user,
        'login': login,
        'lunbos': lunbo,
        'remais': remai,
        'num':num
    }
    return render(request, 'index.html', context)


def product(request,id):
    login = False
    user = ''
    num = 0
    if request.session.get('phone'):
        login = True
        phone = request.session.get('phone')
        user = Users.objects.get(phone=phone)
        num = checkNum(phone)
    prod = ReMaiTu.objects.get(id=id)
    context = {
        'prod':prod,
        'login':login,
        'user':user,
        'num':num
    }
    return render(request,'product_details.html',context)
