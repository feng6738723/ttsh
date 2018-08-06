

from django.db import models

from db.base_model import BaseModel


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='名字')  # 名称
    password = models.CharField(max_length=256, verbose_name='密码')   # 密码
    email = models.EmailField(max_length=64, unique=True, verbose_name='邮箱')  # 邮箱
    # False 代表女
    sex = models.BooleanField(default=False, verbose_name='性别')  # 性别
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')  # 是否删除

    class Meta:
        db_table = 'tt_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class UserTicket(models.Model):
    user = models.ForeignKey(User, verbose_name='所属账户')
    ticket = models.CharField(max_length=256, verbose_name='账号密码')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tt_users_ticket'


class AddressManager(models.Manager):
    # 收货地址模型管理器类

    # 1.改变原有查询的结果集:all()
    # 2.封装方法:用户操作模型类对应的数据表(增删改查)

    def get_default_address(self, user):
        try:
            '''获取用户默认收货地址'''
            # self.model:获取self对象所在的模型类
            addr = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # 默认不存在收货地址
            addr = None

        return addr


class Address(BaseModel):
    # 收货地址模型类
    user = models.ForeignKey(User, verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义模型管理器
    objects = AddressManager()

    class Meta:
        db_table = 'tt_address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '收件人:%s-地址:%s-电话:%s-默认地址:%s' % (self.receiver, self.addr, self.phone, self.is_default)