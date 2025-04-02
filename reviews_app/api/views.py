from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ReviewSerializer
from .permissions import IsCustomerUser, IsReviewer
from reviews_app.models import Review


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    pagination_class = None

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        return queryset


    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        reviewer = self.request.user
        business_user = serializer.validated_data['business_user']
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Du hast bereits eine Bewertung für diesen Geschäftsnutzer abgegeben.")
        serializer.save(reviewer=reviewer)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewer]
