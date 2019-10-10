import json
import os
from datetime import datetime

from alipay import AliPay
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection

from common.func import checkNum
from content.models import ReMaiTu
from orders.models import Order, OrderDetail
from user.models import Users


def order(request):

    #判断用户是否登录
    if not request.session.get('phone'):
        return redirect(reverse('user:login'))

    #生成订单逻辑
    #取出redis中购物数据
    redis_cli = get_redis_connection('cart')
    phone = request.session.get('phone')
    cart_data = redis_cli.get(f'cart-{phone}')
    # print('cart_data=',cart_data)
    cart_data = json.loads(cart_data)

    cart_dict = {}
    for cart in cart_data:
        if cart_data[cart]['selected'] == '1':
            # {'gid1':'count1', 'gid2':'count2'}
            cart_dict[int(cart)] = int(cart_data[cart]['num'])

    # print('cart_dict=',cart_dict)
    #生成总订单逻辑
    user = Users.objects.get(phone=phone)

    #生成订单号
    order_code = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)

    order = Order.objects.create(
        uid=user.id,
        order_code=order_code,
        total_count=sum(cart_dict.values()),
        total_amount=0,
        status=1
    )

    #生成子订单

    totalcount = 0
    for gid,count in cart_dict.items():

        good = ReMaiTu.objects.get(id=gid)

        OrderDetail.objects.create(
            uid=user.id,
            order_code=order_code,
            goods_id=gid,
            counts=count,
            price=good.price1
        )

        totalcount += count * good.price1

        #清除redis中数据
        del cart_data[str(gid)]

    order.total_amount = totalcount
    order.save()

    #重新添加redis数据
    redis_cli.set(f'cart-{phone}',json.dumps(cart_data))


    return redirect(reverse('orders:noy_pay'))


def noy_pay(request):
    if request.session.get('phone'):

        phone = request.session.get('phone')
        user = Users.objects.get(phone=phone)
        orders = Order.objects.filter(uid=user.id,status=1)
        data_dict = {}
        total_price = 0
        for order in orders:
            data_list = []
            order_details = OrderDetail.objects.filter(order_code=order.order_code)
            for order_detail in order_details:
                good = ReMaiTu.objects.get(id=order_detail.goods_id)
                data = {
                    'img':good.img,
                    'name':good.mane,
                    'price':order_detail.price,
                    'num':order_detail.counts,
                    'total_amount':order.total_amount
                }
                data_list.append(data)
            data_dict[order.order_code] = data_list
            total_price += order.total_amount

        num = checkNum(phone)
        context = {
            'data_dict':data_dict,
            'login':True,
            'user':user,
            'total_price':total_price,
            'num':num
        }

        return render(request, 'noy_pay.html', context)
    else:
        return redirect(reverse('user:login'))





def pay(request, order_code):

    alipay = AliPay(
        appid='2016092700609211',
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "alipay/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "alipay/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )

    order = Order.objects.get(order_code=order_code)

    # 生成登录支付宝连接
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_code,
        total_amount=float(order.total_amount),
        subject='商品支付信息',
        return_url='http://127.0.0.1:8000/payback/',
    )

    alipay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return redirect(alipay_url)



# 支付宝回调接口
def payback(request):

    query_dict = request.GET
    data = query_dict.dict()

    # 获取并从请求参数中剔除signature
    signature = data.pop('sign')

    # 创建支付宝支付对象
    alipay = AliPay(
        appid='2016092700609211',
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "alipay/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "alipay/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )

    # 校验这个重定向是否是alipay重定向过来的
    success = alipay.verify(data, signature)
    if success:
        order_code = data['out_trade_no']
        Order.objects.filter(order_code=order_code).update(status=2)
        return redirect(reverse('orders:not_rev'))
    else:
        # 验证失败
        return HttpResponse('支付失败')


def not_rev(request):
    if request.session.get('phone'):

        phone = request.session.get('phone')
        user = Users.objects.get(phone=phone)
        orders = Order.objects.filter(uid=user.id, status=2)
        data_dict = {}
        total_price = 0
        for order in orders:
            data_list = []
            order_details = OrderDetail.objects.filter(order_code=order.order_code)
            for order_detail in order_details:
                good = ReMaiTu.objects.get(id=order_detail.goods_id)
                data = {
                    'img': good.img,
                    'name': good.mane,
                    'price': order_detail.price,
                    'num': order_detail.counts,
                    'total_amount': order.total_amount
                }
                data_list.append(data)
            data_dict[order.order_code] = data_list
            total_price += order.total_amount
        num = checkNum(phone)
        context = {
            'data_dict': data_dict,
            'login': True,
            'user': user,
            'total_price': total_price,
            'num':num
        }

        return render(request, 'not_rev.html', context)
    else:
        return redirect(reverse('user:login'))