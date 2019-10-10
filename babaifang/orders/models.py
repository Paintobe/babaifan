from django.db import models

# Create your models here.

# 订单总表
class Order(models.Model):
    uid = models.IntegerField(verbose_name="用户id")
    order_code = models.CharField(max_length=100, verbose_name="订单编号")
    total_count = models.IntegerField(verbose_name="订单总数量")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单总金额")
    status = models.SmallIntegerField(verbose_name="1为未支付，2为未发货，3为未收货")

    class Meta:
        db_table = 'axf_order'



# 订单子表
class OrderDetail(models.Model):
    uid = models.IntegerField(verbose_name="用户id")
    order_code = models.CharField(max_length=100, verbose_name="订单编号")
    goods_id = models.IntegerField(verbose_name="商品id")
    counts = models.IntegerField(verbose_name="商品数量")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品单价")

    class Meta:
        db_table = 'axf_order_detail'
