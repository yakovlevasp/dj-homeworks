from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Advertisement, AdvertisementStatusChoices, FavoriteAds
from .serializers import AdvertisementSerializer, FavoriteAdsSerializer
from .filters import AdvertisementFilter
from .permissions import IsAdminOrOwner


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """Список объявлений. Черновики показываются только автору"""

        return Advertisement.objects.filter(
            ~Q(status=AdvertisementStatusChoices.DRAFT) | Q(creator_id=self.request.user.id)
        )

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy", "favorite"]:
            return [IsAuthenticated(), IsAdminOrOwner()]
        return []

    @action(detail=False, methods=['get'])
    def favorite(self, request):
        """Список избранных объявлений"""

        favorite_ads = FavoriteAds.objects.values_list('ad', flat=True).filter(user=request.user.id)
        ads_qs = Advertisement.objects.filter(id__in=favorite_ads)
        serializer = AdvertisementSerializer(self.filter_queryset(ads_qs), many=True)
        return Response(serializer.data)


class FavoriteAdsView(CreateAPIView, DestroyAPIView):
    """
    View для избранных объявлений
    """
    queryset = FavoriteAds.objects.all()
    serializer_class = FavoriteAdsSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)
