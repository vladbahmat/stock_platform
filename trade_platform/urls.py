from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views
from trade_platform.views import InventoryView, WatchListView, ItemView, OfferView, PositionView, WorkShiftView, \
    StripeView
from trade_platform.views.user import UserView

app_name = 'trade_platform'
router = routers.DefaultRouter()
router.register(r'inventory', InventoryView, basename='inventory')
router.register(r'watchlist', WatchListView, basename='watchlist')
router.register(r'offer', OfferView, basename='offer')
router.register(r'item', ItemView, basename='item')
router.register('position', PositionView, basename='position')
router.register('workshift', WorkShiftView, basename='workshift')
router.register('stripe', StripeView, basename='stripe')
router.register('user', UserView, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('login', views.TokenObtainPairView.as_view()),
]