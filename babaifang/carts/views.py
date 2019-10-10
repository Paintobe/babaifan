import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

# Create your views here.
from django.urls import reverse

from common.func import checkNum
from content.models import ReMaiTu
from user.models import Users


def cart(request):
    if request.session.get('phone'):
        redis_cli = get_redis_connection('cart')
        login = True
        phone = request.session.get('phone')
        user = Users.objects.get(phone=phone)
        dataall = redis_cli.get(f'cart-{phone}')
        num = checkNum(phone)
        if not dataall:
            dataall = ''
        else:
            dataall = json.loads(dataall)
        context = {
            'login':login,
            'user':user,
            'dataall':dataall,
            'num':num
        }
        return render(request,'cart.html',context)
    else:
        return redirect(reverse('contents:index'))



# {'phone':{id:{'prod':'','num':''},id:{}}}
def savadata(request):
    phone = request.session.get('phone')
    id = request.POST.get('id')
    selected = request.POST.get('selected', '1')  # 默认选中
    # print(selected)
    # print('id=',id)
    prod = ReMaiTu.objects.get(id=int(id))
    num = request.POST.get('num')
    #redis中查询数据
    redis_cli = get_redis_connection('cart')
    dataall = redis_cli.get(f'cart-{phone}')
    # print(dataall)

    #将该商品添加进去，没有新增，有则覆盖
    if not dataall:
        dataall = {id:{'selected':selected,'num':num,'price':str(prod.price1),'img':prod.img,'name':prod.mane,'price2':str(prod.price2)}}
        dataall = json.dumps(dataall)
        redis_cli.set(f'cart-{phone}',dataall)
    else:
        dataall = json.loads(dataall)
        dataall[id] = {'selected':selected,'num':num,'price':str(prod.price1),'img':prod.img,'name':prod.mane,'price2':str(prod.price2)}
        if num == '0':
            del dataall[id]
        dataall = json.dumps(dataall)
        redis_cli.set(f'cart-{phone}', dataall)
    dataall = json.loads(dataall)
    allnum = 0
    for k,v in dataall.items():
        allnum += int(v['num'])

    # print(dataall)
    # print(allnum)

    return JsonResponse({'allnum':allnum})


def selects(request):
    selected = request.POST.get('selected')
    # print(selected)
    phone = request.session.get('phone')
    # redis中查询数据
    redis_cli = get_redis_connection('cart')
    dataall = redis_cli.get(f'cart-{phone}')
    dataall = json.loads(dataall)
    # print(dataall)
    for k,v in dataall.items():
        v['selected'] = selected
    dataall = json.dumps(dataall)
    redis_cli.set(f'cart-{phone}', dataall)
    # print(redis_cli.get(f'cart-{phone}'))
    return HttpResponse({'data':'ok'})


def remove(request):
    id = request.POST.get('id')
    # print(id)
    # print(type(id))
    phone = request.session.get('phone')
    # redis中查询数据
    redis_cli = get_redis_connection('cart')
    dataall = redis_cli.get(f'cart-{phone}')
    dataall = json.loads(dataall)
    # print(dataall)

    del dataall[id]
    if dataall != '':
        dataall = json.dumps(dataall)
        # print(dataall)
    redis_cli.set(f'cart-{phone}', dataall)
    return HttpResponse({'data':'ok'})


def removeall(request):
    phone = request.session.get('phone')
    # redis中查询数据
    redis_cli = get_redis_connection('cart')
    dataall = {}
    dataall = json.dumps(dataall)
    redis_cli.set(f'cart-{phone}',dataall)
    return HttpResponse('ok')
