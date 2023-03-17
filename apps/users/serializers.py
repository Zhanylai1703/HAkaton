from djoser.serializers import UserCreateSerializer,  UserSerializer 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Department





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
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'avatar' )

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'user']





    
