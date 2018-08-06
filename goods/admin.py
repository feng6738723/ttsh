
from django.contrib import admin
from goods.models import *


admin.site.site_header = '生鲜管理后台'


class GoodsSKUInLine(admin.ModelAdmin):
    model = GoodsSKU


class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete']
    list_filter = ['is_delete']
    list_per_page = 20


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 20


class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'goods', 'price', 'stock', 'sales']
    list_filter = ['status', 'goods', 'type']
    list_per_page = 20


class IndexGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'index']
    list_per_page = 20


class IndexPromotionBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'index']
    list_per_page = 20


class IndexTypeGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'sku', 'index', 'display_type']
    list_filter = ['type']
    list_per_page = 20


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(Goods, GoodsAdmin)
