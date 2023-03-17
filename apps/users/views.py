from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from djoser.views import UserViewSet
from .serializers import (RegisterSerializer, 
                          LoginSerializer, UserSerializer, 
                          DepartmentSerializer, 
                          ResetPasswordSerializer)
from .models import User, Department
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import jwt
from django.conf import settings
from rest_framework import status




User = get_user_model()


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
        response_data = {
            'user_id': user.id,
            'tokens': tokens

        }
        return Response(
            response_data,
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


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this email'}, status=400)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            send_mail(
                'Password Reset Request',
                f'Ваш новый пароль  {password}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'success': 'Password reset email has been sent'})
        return Response({'error': 'Email field is required'}, status=400)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]




class CurrentUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        return UserSerializer




class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = []
