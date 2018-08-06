# from django.utils.deprecation import MiddlewareMixin
#
#
# class UserMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # 需要登录验证，个人中心和购物车和商品的增删
#         need_login = ['/axf/mine/', '/axf/addCart/',
#                       '/axf/subCart/', '/axf/cartweb/',
#                       '/axf/generateOrder/', '/axf/waitPay/',
#                       '/axf/payed/', '/axf/countPrice/',
#                       '/axf/changeCartAllSelect/']
#         if request.path in need_login:
