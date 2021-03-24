from django.contrib import admin
from django.conf.urls import url, include
from rest_framework_simplejwt import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('/', include('trade_platform.urls')),
]
