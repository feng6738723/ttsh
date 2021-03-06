"""ttfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static

from ttfresh import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^userweb/', include('user.urls', namespace='userweb')),
    url(r'^cartweb/', include('cart.urls', namespace='cartweb')),
    url(r'^/', include('goods.urls', namespace='goods')),
    url(r'^orderweb/', include('order.urls', namespace='orderweb')),
    url(r'^backweb/', include('backweb.urls', namespace='backweb')),
    url(r'^goodweb/', include('goods.urls', namespace='goodweb')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
