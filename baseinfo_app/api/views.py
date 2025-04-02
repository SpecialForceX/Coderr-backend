from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from reviews_app.models import Review
from users_app.models import CustomUser
from offers_app.models import Offer

class BaseInfoView(APIView):
    permission_classes = []  # öffentlich zugänglich

    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        average_rating = round(average_rating, 1)

        business_profile_count = CustomUser.objects.filter(is_business=True).count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }
        return Response(data, status=status.HTTP_200_OK)
