from django.conf.urls import url

from cart import views

urlpatterns = [
    # 购物车
    url(r'^cart/', views.Cart, name='cart'),
    # 添加购物车
    url(r'^addtocard/', views.AddToCard, name='addtocard'),
    # 删除购物车
    url(r'^subtocard/', views.SubToCard, name='subtocard'),
]