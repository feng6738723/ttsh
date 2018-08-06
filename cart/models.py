
from django.db import models

from goods.models import GoodsSKU
from user.models import User


class CartModel(models.Model):
    user = models.ForeignKey(User, verbose_name='关联用户')  # 关联用户
    goods = models.ForeignKey(GoodsSKU, verbose_name='关联的商品')
    quantity = models.IntegerField(default=1, verbose_name='商品的数量')
    is_select = models.BooleanField(default=True, verbose_name='是否勾选商品')

    class Meta:
        db_table = 'tt_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
