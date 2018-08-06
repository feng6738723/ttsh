from django.conf.urls import url

from backweb import views

urlpatterns = [
    # 购物车
    url(r'^backorder', views.Backorder, name='backorder'),
    url(r'^product_list', views.product_list, name='product_list'),
    url(r'^product_detail', views.product_detail, name='product_detail'),

]