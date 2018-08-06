
from django.shortcuts import render


def Backorder(request):
    if request.method == 'GET':
        return render(request, 'backwebs/order_list.html')


def product_list(request):
    if request.method == 'GET':
        return render(request, 'backwebs/product_list.html')


def product_detail(request):
    if request.method == 'POST':
        user = request.user

        names = request.POST.get('name')
