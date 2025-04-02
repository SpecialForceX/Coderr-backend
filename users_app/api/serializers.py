from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users_app.models import CustomUser

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel',
            'description', 'working_hours', 'type', 'email', 'created_at'
        ]
        read_only_fields = ['username', 'created_at']

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_customer = user_type == 'customer'
        user.is_business = user_type == 'business'
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
