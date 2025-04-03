from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import OrderSerializer
from .permissions import IsCustomerUser, IsBusinessUser, IsAdminUser
from orders_app.models import Order
from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.views import APIView
from users_app.models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        offer_detail_id = self.request.data.get('offer_detail_id')
        print("RAW DATA:", self.request.data)

        try:
            offer_detail_id = int(offer_detail_id)
        except (ValueError, TypeError):
            raise ValidationError({"offer_detail_id": ["This value must be a number."]})

        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)

        serializer.save(
            customer_user=self.request.user,
            business_user=offer_detail.offer.user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type
        )
    pagination_class = None


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessUser]
    http_method_names = ['patch']


class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class InProgressOrderCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(CustomUser, id=business_user_id)

        if not business_user.is_business:
            return Response({"error": "User is not a business user."}, status=400)

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            user = CustomUser.objects.get(id=business_user_id)
            if user.type != "business":
                return Response({"error": "User is not a business user."}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        completed_count = Order.objects.filter(
            business_user=user,
            status="completed"
        ).count()

        return Response({"completed_order_count": completed_count}, status=status.HTTP_200_OK)

