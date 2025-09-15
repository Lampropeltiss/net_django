from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrAdmin
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['-status', 'creator']

    def get_queryset(self):
        requester = self.request.user
        queryset = Advertisement.objects.all()
        if requester.is_authenticated:
            return queryset.exclude(~Q(creator=requester) & Q(status='DRAFT'))
        else:
            return queryset.exclude(status='DRAFT')

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticatedOrReadOnly()]

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorites',
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        user = request.user
        adv = self.get_object()
        r_line = f"{user=}, {adv=}"

        if request.method == 'POST':
            creator = adv.creator
            if creator == user:
                return Response(
                    {'message': f"You can't add your own advertisements in favorites."}
                )
            try:
                fav = Favorite.objects.get(user=user, adv=adv)
                return Response(
                    {'message': f'This advertisement is already in your favorites.'}
                )
            except ObjectDoesNotExist:
                fav = Favorite.objects.create(user=user, adv=adv)
                return Response(
                    {'message': f'Success.'}
                )

        elif request.method == 'DELETE':
            try:
                fav = Favorite.objects.get(user=user, adv=adv).delete()
                return Response(
                    {'message': f'Success.'}
                )
            except ObjectDoesNotExist:
                return Response(
                    {'message': f'This advertisement is not in your favorites.'}
                )

    @action(
        methods=['GET'],
        detail=False,
        url_path='favorites',
        permission_classes=[IsAuthenticated, ]
    )
    def favorites(self, request):
        user = request.user

        fav_adv_list = Favorite.objects.filter(user=user).prefetch_related('adv').values('adv')
        adv_id_list = [record['adv'] for record in fav_adv_list]
        queryset = Advertisement.objects.filter(id__in=fav_adv_list)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
