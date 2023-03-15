from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from djoser.views import UserViewSet
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User
import jwt
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny ,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        user_payload = {
            'user_id': user.id,
            'username': user.username
        }
        tokens = {
            'access_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256"),
            'refresh_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        }
        return Response(
            tokens,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


