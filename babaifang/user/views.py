import random,re
import requests
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection

from content.models import LunBoTu, ReMaiTu
from user.models import Users


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:

        phone = request.POST.get('account')
        password = request.POST.get('pwd')
        # status = request.POST.get('status')
        #         # print(status)

        if not Users.objects.filter(phone=phone).exists():
            return HttpResponse('账号或密码错误')
        else:
            user = Users.objects.get(phone=phone)
            if check_password(password,user.password):
                request.session['phone'] = phone

                return redirect(reverse('contents:index'))


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        phone = request.POST.get('mobile')
        password1 = request.POST.get('pwd')
        password2 = request.POST.get('pwd2')
        code = request.POST.get('licence')
        code2 = request.POST.get('licence2')
        sms = request.POST.get('mobileLicence')
        # print(phone,password1,password2,code,code2,sms)
        # print(type(phone))
        if not re.match('1[3-9]\d{9}',phone):
            return HttpResponse('手机号格式错误！')
        if not Users.objects.filter(phone=phone).exists():

            if password1 != password2:
                return HttpResponse('密码输入不一致！')
            if code!=code2:
                return HttpResponse('验证码输入错误')

            redis_cli = get_redis_connection()
            if redis_cli.get(f'sms_{phone}').decode() != sms:
                return HttpResponse('手机验证码错误')

            Users.objects.create(
                phone=phone,
                password=make_password(password1)
            )
            return render(request,'login.html')
        else:
            return HttpResponse('此号码已被注册')



# 发送短信
def sendsms(request):
    smscode = random.randint(1000, 9999)
    phone = request.POST.get('phone')

    if not re.match('1[3-9]\d{9}', phone):
        return HttpResponse('手机号格式错误！')

    data = {
        "sid": "8036ece41e07ea5340794286185f9214",
        "token": "8a9c9099eb825ea314bcb620f9fdbc6b",
        "appid": "cceff1236cee4e1e87b87186dc10ad27",
        "templateid": "493813",
        "param": smscode,
        "mobile": phone,
    }

    # 用云之讯第三方发短信
    res = requests.post('https://open.ucpaas.com/ol/sms/sendsms', json=data)

    res = res.json()

    if res['code'] == '000000':

        # 保存验证码，保存在缓存里面，给一个过期时间
        # 实例化redis
        redis_cli = get_redis_connection()

        redis_cli.set(f'sms_{phone}', smscode, 180)

        return JsonResponse({'res': 'yes'})
    else:
        return JsonResponse({'res': 'no'})


# def info(request):
#     if request.session.get('phone'):
#         phone = request.session.get('phone')
#         user = Users.objects.get(phone=phone)
#         login = True
#         lunbo = LunBoTu.objects.all()
#         remai = ReMaiTu.objects.all()
#         context = {
#             'user': user,
#             'login': login,
#             'lunbos': lunbo,
#             'remais': remai
#         }
#         return render(request, 'info.html', context)
#     else:
#         return redirect(reverse('user:login'))


def logout(request):
    del request.session['phone']
    return redirect(reverse('user:login'))