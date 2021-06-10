from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from trade_platform.models import WatchList
from trade_platform.serializers import WatchListSerializer, \
    DetailWatchListSerializer


class WatchListView(viewsets.GenericViewSet,
                    ListModelMixin,
                    UpdateModelMixin,
                    RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = WatchList.objects.all()
    http_method_names = ('get', 'patch')
    serializer_classes_by_action = {
        'list': WatchListSerializer,
        'retrieve': DetailWatchListSerializer,
        'update': WatchListSerializer,
    }

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response("Incorrect request",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, WatchListSerializer)

    @action(detail=False, methods=['get'], url_path='my_watchlist')
    def my_watchlist(self, request, *args, **kwargs):
        queryset = request.user.profile.watchlist
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)