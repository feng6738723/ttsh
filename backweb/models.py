from django.db import models

from db.base_model import BaseModel
from goods.models import Goods
from order.models import OrderInfo, OrderGoods
from user.models import User, Address


class BackGoods(Goods):

    class Meta:
        db_table = 'back_goods'
        # verbose_name = '商品列表'
        # verbose_name_plural = verbose_name


class BackOrderInfo(OrderInfo):
    """订单模型类"""

    class Meta:
        db_table = 'back_order_info'
        # verbose_name = '订单'
        # verbose_name_plural = verbose_name


class BackOrderGoods(OrderGoods):
    """订单商品模型类"""

    class Meta:
        db_table = 'back_order_goods'
        # verbose_name = '订单商品'
        # verbose_name_plural = verbose_name


class BackUser(User):

    class Meta:
        db_table = 'back_users'


class BackAddress(Address):
    # 收货地址模型类

    class Meta:
        db_table = 'back_address'
