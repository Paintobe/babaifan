from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^savadata/$',views.savadata,name='savadata'),
    url(r'^selects/$',views.selects,name='selects'),
    url(r'^remove/$',views.remove,name='remove'),
    url(r'^removeall/$',views.removeall,name='removeall')
]

