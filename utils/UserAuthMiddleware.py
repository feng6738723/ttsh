import re
from datetime import datetime

from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

from django.utils.deprecation import MiddlewareMixin

from user.models import UserTicket


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 如果请求的路径为登录页面和注册页面,
        path = ['/userweb/login/',
                '/userweb/register/',
                ]
        # 就不经过验证
        for path in path:

            if re.match(path, request.path):
                return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('userweb:login'))

        user = UserTicket.objects.filter(ticket=ticket).first()
        if not user:
            return HttpResponseRedirect(reverse('userweb:login'))

        if user.out_time.replace(tzinfo=None) < datetime.now():
            user.delete()
            return HttpResponseRedirect(reverse('userweb:login'))
        request.user = user.user
