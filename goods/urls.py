from django.conf.urls import url

from goods import views

urlpatterns = [
    # 首页
    url(r'^index/', views.Index, name='index'),
    # 商品的详情页
    url(r'^detail/(?P<goods_id>\d+)$', views.detail, name='detail'),
    # 商品的列表页
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', views.list, name='list'),
]