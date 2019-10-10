from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order/$',views.order,name='order'),
    url(r'^noy_pay/$',views.noy_pay,name='noy_pay'),
    url(r'^not_rev/$',views.not_rev,name='not_rev'),
    url(r'^pay/(\d+)/$',views.pay,name='pay'),
    url(r'^payback/$', views.payback, name='payback')
]