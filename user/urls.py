from django.conf.urls import url

from user import views

urlpatterns = [
    # 用户中心页面
    url(r'^my/', views.my, name='my'),
    # 登录页面
    url(r'^login/', views.login, name='login'),
    # 注册页面
    url(r'^register/', views.register, name='register'),
    # 登出页面
    url(r'^logout/', views.logout, name='logout'),
    # 用户中心-收货地址信息
    url(r'^address/', views.address, name='address'),
    # 用户中心-订单信息
    url(r'^userorder/', views.userorder, name='userorder'),
]
