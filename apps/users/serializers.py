from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    class Meta:
        fields = (
            'access_token',
            'refresh_token',
        )

class RegisterSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User does not exist.")
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

# class UserSerializer(serializers.UserSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email',)

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        fields = ('id', 'username', 'email',)

