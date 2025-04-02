from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferSerializer, OfferListSerializer, OfferDetailSerializer
from users_app.api.permissions import IsBusinessUser, IsOwner

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().prefetch_related('details', 'user')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['user', 'user__id']
    ordering_fields = ['updated_at']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
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
    permission_classes = [AllowAny]
    lookup_field = 'pk' 