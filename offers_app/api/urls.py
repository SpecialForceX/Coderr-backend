# urls.py in offers_app/api

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, OfferDetailView

router = DefaultRouter()
router.register('', OfferViewSet, basename='offers')

offer_urls = [
    path('', include(router.urls)),
]

offerdetail_urls = [
    path('<int:pk>/', OfferDetailView.as_view({'get': 'retrieve'}), name='offerdetail-detail'),
]

