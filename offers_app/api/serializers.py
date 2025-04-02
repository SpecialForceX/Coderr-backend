from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from users_app.models import CustomUser


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        exclude = ['offer']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'user_details'
        ]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()

            for detail in details_data:
                OfferDetail.objects.create(offer=instance, **detail)

        return instance

    
class OfferDetailReadOnlySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/api/offers/offerdetails/{obj.id}/'



class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailReadOnlySerializer(many=True, read_only=True)
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]


