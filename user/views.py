from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.models import User, UserTicket
from utils.functions import get_ticket


def my(request):

    if request.method == 'GET':
        return render(request, 'userweb/user_center_info.html')


def register(request):
    # 注册
    if request.method == 'GET':
        return render(request, 'userweb/register.html')
    if request.method == 'POST':
        # 先从前端获取所需要的值
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # 进行数据非空的验证,如果注册中数据出现空的情况,返回指定的页面
        if not all([username, password, email]):
            data = {
                'msg': '请将数据填写完整'
            }
            return render(request, 'userweb/register.html', data)
        # 校验注册的用户名是否存在
        if User.objects.filter(username=username):
            data = {
                'msg': '用户名已存在'
            }
            return render(request, 'userweb/register.html', data)
        # 创建密码
        password = make_password(password)

        # 进行用户的创建,将获取的值带入到用户表中进行存储
        User.objects.create(username=username, password=password,
                            email=email,)
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    # 登录
    if request.method == 'GET':
        return render(request, 'userweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        # 检验登录时的数据是否完整
        if not all([username, password]):
            data['msg'] = '请填入完整的信息'
        # 判断用户是否存在数据库中, exists判断结果是否存在,返回为true(存在)或者false(不存在)
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                res = HttpResponseRedirect(reverse('url:my'))
                # 获取cookie值
                ticket = get_ticket()
                out_time = datetime.now() + timedelta(days=30)
                res.set_cookie('ticket', ticket ,expires=out_time)
                # 将cookie值存到数据库中
                UserTicket.objects.create(user=user, ticket=ticket, out_time=out_time)
                return res
            else:
                data['msg'] = '密码错误'

        else:
            data['msg'] = '用户名错误'
        # 返回用户登录的页面
        return render(request, 'userweb/login.html', data)


def logout(request):
    # 登出
    request.session.flush()
    return redirect('/')


def address(request):
    # 用户的收货地址信息
    if request.method == 'GET':
        return render(request, 'userweb/user_center_site.html')


def userorder(request):
    # 用户的订单中心
    if request.method == 'GET':
        return render(request, 'userweb/user_center_order.html')