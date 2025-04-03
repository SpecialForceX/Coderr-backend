from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferSerializer, OfferListSerializer, OfferDetailSerializer
from users_app.api.permissions import IsBusinessUser, IsOwner
from django.db.models import Min
from rest_framework.exceptions import ValidationError


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().prefetch_related('details', 'user')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['user', 'user__id']
    ordering_fields = ['updated_at']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Offer.objects.all().prefetch_related('details', 'user')
        queryset = queryset.annotate(real_min_price=Min('details__price'))

        creator_id = self.request.query_params.get('creator_id')
        if creator_id not in [None, '']:
            try:
                creator_id = int(creator_id)
                queryset = queryset.filter(user__id=creator_id)
            except ValueError:
                raise ValidationError({"creator_id": "This value must be a number."})

        min_price = self.request.query_params.get('min_price')
        if min_price not in [None, '']:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(real_min_price__gte=min_price)
            except ValueError:
                raise ValidationError({"min_price": "This value must be a number."})

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time not in [None, '']:
            try:
                max_delivery_time = int(max_delivery_time)
                queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time).distinct()
            except ValueError:
                raise ValidationError({"max_delivery_time": "This value must be a number."})

        return queryset


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferDetailView(viewsets.ReadOnlyModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk' 