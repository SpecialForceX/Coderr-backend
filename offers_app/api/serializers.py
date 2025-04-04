from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from users_app.models import CustomUser
from django.db.models import Min 


class OfferDetailSerializer(serializers.ModelSerializer):
    offer_type = serializers.CharField()
    class Meta:
        model = OfferDetail
        exclude = ['offer']

    def validate_offer_type(self, value):
        valid_choices = [choice[0] for choice in OfferDetail._meta.get_field("offer_type").choices]
        if value not in valid_choices:
            raise serializers.ValidationError([
                f"'{value}' is not a valid choice.",
                f"Valid options are: {', '.join(valid_choices)}."
            ])

        return value



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'user_details',
            'min_price', 'min_delivery_time'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']

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
            if not details_data:
                raise serializers.ValidationError({"details": "Details dürfen nicht leer sein."})

            validated_details = []
            for detail in details_data:
                detail_serializer = OfferDetailSerializer(data=detail)
                detail_serializer.is_valid(raise_exception=True)
                validated_details.append(detail_serializer.validated_data)

            instance.details.all().delete()
            for valid_detail in validated_details:
                OfferDetail.objects.create(offer=instance, **valid_detail)


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


