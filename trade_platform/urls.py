from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views

from trade_platform.views import InventoryView, WatchListView, ItemView, OfferView

app_name = 'trade_platform'
router = routers.DefaultRouter()
router.register(r'inventory', InventoryView, basename='inventory')
router.register(r'watchlist', WatchListView, basename='watchlist')
router.register(r'offer', OfferView, basename='offer')
router.register(r'item', ItemView, basename='item')


urlpatterns = [
    path('', include(router.urls)),
    path('login', views.TokenObtainPairView.as_view()),
]