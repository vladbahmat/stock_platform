from django.contrib import admin
from django.conf.urls import url, include, re_path
from django.urls import path
from rest_framework import permissions

from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
    url='http://127.0.0.1:8000/',
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('admin/', admin.site.urls, name='admin'),
    re_path('/', include('trade_platform.urls'), name='trade_platform'),
    re_path(r'api/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
