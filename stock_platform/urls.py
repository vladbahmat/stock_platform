from django.contrib import admin
from django.conf.urls import url, include, re_path
from django.urls import path

urlpatterns = [
    re_path('admin/', admin.site.urls, name='admin'),
    re_path('/', include('trade_platform.urls'), name='trade_platform'),
]
