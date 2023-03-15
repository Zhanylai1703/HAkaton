from rest_framework import serializers

from users.models import User


class UserTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    class Meta:
        fields = (
            'access_token',
            'refresh_token',
        )


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
