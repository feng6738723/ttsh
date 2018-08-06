from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, GoodsSKU
from order.models import OrderGoods


def Index(request):
    if request.method == 'GET':
        # 获取商品的种类信息
        types = GoodsType.objects.all()
        # 获取首页banner
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')
        # 获取分类商品的展示信息
        for type_list in types:
            # 获取分类商品中的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type_list, display_type=1).order_by('index')
            # 获取分类商品中的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type_list, display_type=0).order_by('index')

            type_list.image_banners = image_banners
            type_list.title_banners = title_banners
        data = {
            'types': types,
            'goods_banners': goods_banners,
        }

        return render(request, 'goodweb/index.html', data)


def detail(request, goods_id):

    if request.method == 'GET':
        sku = GoodsSKU.objects.get(id=goods_id)

        # 获取商品分类信息
        types = GoodsType.objects.all()

        # 获取商品的评论信息
        sku_order_comment = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 获取新品信息，添加时间最晚的两个为新品
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]
        # 获取同类商品信息
        same_sku = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)
        data = {
            'types': types,
            'sku_order_comment': sku_order_comment,
            'new_skus': new_skus,
            'same_sku': same_sku,
            'sku': sku,

        }
        return render(request, 'goodweb/detail.html', data)


def list(request, type_id, page):
    if request.method == 'GET':

        # 根据type_id获取商品种类信息
        try:
            good_type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 种类不存在
            return redirect('/')

        # 获取商品的分类信息
        good_types = GoodsType.objects.all()

        # 获取排序的方式 # 获取分类商品的信息
        # sort=default 按照默认id排序
        # sort=price 按照商品价格排序
        # sort=hot 按照商品销量排序
        sort = request.GET.get('sort')

        if sort == 'price':
            skus_list = GoodsSKU.objects.filter(type=good_type).order_by('price')
        elif sort == 'hot':
            skus_list = GoodsSKU.objects.filter(type=good_type).order_by('-sales')
        else:
            sort = 'default'
            skus_list = GoodsSKU.objects.filter(type=good_type).order_by('-id')

        # 创建分页对象 每页4条
        paginator = Paginator(skus_list, 4)

        try:
            page = int(page)
        except:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的数据
        skus_page = paginator.page(page)

        #  进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页

        # 获取分页总数
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page >= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 获取新品的信息
        news_sku = GoodsSKU.objects.filter(type=good_type).order_by('-create_time')[:2]

        # user = request.user
        # cart_count = 0
        # if user.is_authenticated():
        #     # 获取购物车的商品数量
        #     conn = get_redis_connection('default')
        #     cart_key = 'cart_%d' % user.id
        #     cart_count = conn.hlen(cart_key)

        data = {
            # 'cart_count': cart_count,
            'good_type': good_type,
            'types': good_types,
            'skus_page': skus_page,
            'news_sku': news_sku,
            'pages': pages,
            'sort': sort
        }
        return render(request, 'goodweb/list.html', data)
