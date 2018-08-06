from django.conf.urls import url

from order import views
urlpatterns = [
    # 下单
    url(r'^orderweb/', views.order, name='orderweb'),
    # 商品支付的页面
    url(r'^orderinfo/', views.orderinfo, name='orderinfo'),
    # 修改订单的状态
    url(r'^changeorderstatus/', views.changeorderstatus, name='changeorderstatus'),
    # 待收货
    url(r'^payed/', views.payed, name='payed'),
    # 待付款
    url(r'^waitpay/', views.waitpay, name='waitpay')
]