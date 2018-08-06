from django.http import JsonResponse
from django.shortcuts import render

from cart.models import CartModel
from goods.models import GoodsSKU


def Cart(request):
    # 购物车
    if request.method == 'GET':
        user = request.user
        skus = CartModel.objects.filter(user=user)

        return render(request, 'cartweb/cart.html', {'skus': skus})


def AddToCard(request):
    if request.method == 'POST':
        # 先进行验证用户是否已经登录
        user = request.user
        data = {}
        # 定义一个错误码的对应的文档
        data['code'] = '1992'
        # 如果用户已经登录，就获取用户的id
        if user.id:
            # 获取前端获得的商品的id号
            sku_id = request.POST.get('sku_id')
            count = request.POST.get('count')
            # 然后验证当前的用户是否对商品进行添加操作，对数据库进行查看
            cart = CartModel.objects.filter(user=user, sku_id=sku_id).first()
            # 如果有数据
            if cart:
                # 如果是进行添加操作，则对操作进行加1操作
                cart.quantity += 1
                cart.save()
                data['quantity'] = cart.quantity
                # 如果没有的话，是进行首次的添加操作，
            else:
                CartModel.objects.create(user=user, sku_id=sku_id)
                data['quantity'] = 1
            data['code'] = '200'
            data['msg'] = '请求成功'
            return JsonResponse(data)
        return JsonResponse(data)


def SubToCard(request):
    # 删除购物车
    if request.method == 'POST':
        user = request.user
        data = {}
        data['msg'] = '请求成功'
        # 定义一个错误码的对应的文档
        data['code'] = '1993'
        # 如果用户已经登录，就获取用户的id
        if user.id:
            # 获取前端获得的商品的id号
            sku_id = request.POST.get('sku_id')
            # 然后验证当前的用户是否对商品进行添加操作，对数据库进行查看
            card = CartModel.objects.filter(user=user, sku_id=sku_id).first()
            # 如果存在数据的话
            if card:
                # 如果数据的数量是1，那么对数据进行操作后，数据将会被删除，变为0
                if card.quantity == 1:
                    card.delete()
                    data['quantity'] = 0
                # 如果数量不是1的时候，那么操作的时候就会对数据进行减一的操作
                else:
                    card.quantity -= 1
                    card.save()
                    data['quantity'] = card.quantity
                # 定义一个代码的返回code的成功数值
                data['code'] = '200'
                return JsonResponse(data)
            # 如果数据不存在，就给返回一个数据信息
            else:
                data['msg'] = '请先添加商品'
                return JsonResponse(data)
        # 如果用户没有登录。
        else:
            data['msg'] = '用户没有登录'
            return JsonResponse(data)

