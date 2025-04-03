from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from .permissions import IsProfileOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny


User = get_user_model()

from rest_framework.response import Response

class NoPagination(PageNumberPagination):
    page_size = 100000

class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_permissions(self):
        return [IsAuthenticated(), IsProfileOwner()]


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BusinessProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(is_business=True)

class CustomerProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(is_customer=True)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
            return Response({'detail': 'Ungültige Anmeldedaten.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
