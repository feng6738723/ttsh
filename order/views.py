from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from cart.models import CartModel
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from user.models import Address
from utils.functions import get_order_num


def create(request):
    # 订单页面
    if request.method == 'POST':
        user = request.user
        # 若是从商品详情页进入订单,获取商品的数量和商品id
        count = request.get('count')
        sku_id = request.get('sku_id')
        # 校验参数是否为空
        if not all([count, sku_id]):
            return JsonResponse({'res': 0, 'msg': '数据错误'})

        # 获取商品的列表
        skus = []
        # 获取购物车中商品的总数量和总价
        total_count = 0
        total_price = 0

        # 根据id, 获取商品的信息
        sku = GoodsSKU.objects.get(id='sku_id')

        # 计算商品的小计
        amount = sku.price * int(count)
        # 给商品对象动态的添加小计和数量属性
        sku.amount = amount
        sku.count = count

        # 计算订单商品的总价和数量
        skus.append(sku)
        total_count += int(count)
        total_price += amount

        # 运费
        transit_price = 0

        # 实际付款
        total_pay = transit_price + total_price

        # 添加订单的收货地址
        addrs = Address.objects.filter(user=user)

        data = {
            'sku_id': sku_id,
            'count': count,
            'skus': skus,
            'total_count': total_count,
            'total_price': total_price,
            'total_pay': total_pay,
            'transit_price': transit_price,
            'addrs': addrs
        }
        return render(request, 'orderweb/place_order.html', data)

    if request.method == 'POST':
        user = request.user

        # 若是从购物车进入提交订单页,获取提交的商品sku
        sku_ids = request.POST.getlist('sku_ids')
        if not sku_ids:
            return redirect(reverse('cart:create'))
        # 商品列表
        skus = []
        # 购物车中商品总数量，总价
        total_count = 0
        total_price = 0

        # 遍历商品信息
        for sku_id in sku_ids:
            # 根据id,获取商品信息
            sku = GoodsSKU.objects.get(id=sku_id)
            count = CartModel.objects.filter(user=user, is_select=True)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给商品对象增加小计属性
            sku.amount = amount
            # 动态增加商品数量的属性
            sku.count = count

            skus.append(sku)
            total_count += int(count)
            total_price += amount

        # 运费
        transit_price = 0

        # 实际付款
        total_pay = transit_price + total_price

        # 收货地址
        addrs = Address.objects.filter(user=user)

        sku_ids = ','.join(sku_ids)
        data = {
            'sku_ids': sku_ids,
            'skus': skus,
            'total_count': total_count,
            'total_price': total_price,
            'total_pay': total_pay,
            'addrs': addrs,
            'transit_price': transit_price
        }
        return render(request, 'orderweb/place_order.html', data)


def commit(request):
    # 提交订单
    # 判断是否登录
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'errmsg': '请登录'})

    # 获取数据
    # sku_ids:  '1,2,3'
    sku_ids = request.POST.get('sku_ids')
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')

    # 检验数据
    if not all([sku_ids, addr_id, pay_method]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    if pay_method not in OrderInfo.PAY_METHODS.keys():
        return JsonResponse({'res': 2, 'errmsg': '选择的支付方式错误'})

    # 检查地址
    try:
        addr = Address.objects.get(id=addr_id)
    except Exception:
        return JsonResponse({'res': 3, 'errmsg': '收货地址不正确'})

    # 创建节点
    save_id = transaction.savepoint()
    # 创建订单
    try:
        # 订单id:时间+用户id:20180620182030+id
        order_id = get_order_num()

        # 运费
        transit_price = 0

        # 总数和总金额
        total_count = 0
        total_price = 0

        # 创建一条订单记录
        order = OrderInfo.objects.create(order_id=order_id,
                                         user=user,
                                         addr=addr,
                                         pay_method=pay_method,
                                         total_count=total_count,
                                         total_price=total_price,
                                         transit_price=transit_price)

        sku_ids = sku_ids.split(',')
        for sku_id in sku_ids:
            for i in range(3):
                # 乐观锁
                # 当数据更新的的时候，采取判断此数据是否更改
                try:
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    # 回滚到节点
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

                # 从redis中获取用户所要购买的商品数量
                count = CartModel.objects.filter(user=user, is_select=True)

                # 想order_goods表中添加一条记录
                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=sku.price)

                # 更新商品库存和销量
                orgin_stock = sku.stock
                new_stock = orgin_stock - int(count)
                new_sales = sku.sales + int(count)

                # 返回受影响的行数
                res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                if res == 0:
                    # 如果受影响的行数为0,则说明此数据已经被修改，重新进行库存更新
                    # 防止并发
                    if i == 2:
                        # 尝试三次
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
                    continue

                # 累加计算订单商品的总数量和总价格
                amount = sku.price * int(count)
                total_count += int(count)
                total_price += amount

                # 跳出循环
                break

            # 更新订单信息表中的商品的总数量和总价格
            order.total_price = total_price
            order.total_count = total_count
            order.save()

    except Exception:
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res': 7, 'errmsg': '下单失败'})

    # 提交到数据库
    transaction.savepoint_commit(save_id)

    # 删除购物车中已经下单的商品信息
    order.delete()

    return JsonResponse({'res': 5, 'errmsg': '创建成功'})


def pay(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '请登录'})
        # 从前端获取商品的id号
        order_id = request.POST.get('order_id')
        # 从商品的ID号取到关联的商品名称
        sku = OrderGoods.objects.filter(order_id=order_id)
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的订单'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单不存在'})
        order.save()
        return JsonResponse({'res': 3, 'errmsg': '支付成功', 'sku': sku})






