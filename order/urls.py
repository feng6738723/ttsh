from django.conf.urls import url

from order import views
urlpatterns = [
    # 创建订单操作
    url(r'^orderweb/', views.create, name='create'),
    # 提交订单,生成订单数据
    url(r'^commit/', views.commit, name='commit'),
    # 订单支付页面
    url(r'^pay/', views.pay, name='pay'),

]
