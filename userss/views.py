from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserEmailSerializer, UserTokenSerializer


class UserEmailRegistration(generics.CreateAPIView):
    serializer_class = UserEmailSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = RefreshToken.for_user(user)
        headers = self.get_success_headers(serializer.data)

        tokens = {
            'access_token': str(tokens.access_token),
            'refresh_token': str(tokens)
        }
        return Response(
            tokens,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserAuthTest(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserEmailSerializer
    permission_classes = [IsAuthenticated]
