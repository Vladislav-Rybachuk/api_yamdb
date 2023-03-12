from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .permissions import IsAdministator
from users.serializers import (SignUpUserSerializer,
                               GetJwtTokenSerializer,
                               UserSerializer)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import MethodNotAllowed


account_activation_token = PasswordResetTokenGenerator()


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up_user(request):
    serializer = SignUpUserSerializer(data=request.data)

    if serializer.is_valid():
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        current_user = User.objects.create_user(username=username, email=email)
        confirm_code = account_activation_token.make_token(current_user)
        send_mail('Confirmation of registration',
                  f'your code: {confirm_code}',
                  'yamdb@ya.ru',
                  [email],
                  fail_silently=False,)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = GetJwtTokenSerializer(data=request.data)
    if serializer.is_valid():
        current_user = get_object_or_404(
            User, username=request.data.get('username'))
        if (account_activation_token.check_token(
                token=request.data.get('confirmation_code'),
                user=current_user) is True):

            return Response(get_tokens_for_user(current_user))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([permissions.IsAuthenticated, IsAdministator])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        username = self.kwargs.get('username')
        if self.request.method == 'PUT':
            raise MethodNotAllowed('PUT')

        if username == 'me' and (self.request.method == 'GET'
                                 or self.request.method == 'PATCH'):
            return self.request.user

        if username == 'me' and self.request.method == 'DELETE':
            raise MethodNotAllowed('DELETE')
        current_user = get_object_or_404(User, username=username)
        return current_user

    def perform_update(self, serializer):
        username = self.kwargs.get('username')

        if (username == 'me'
                and serializer.instance.role != self.request.data.get('role')):
            serializer.save(role=serializer.instance.role)
        else:
            super(UserViewSet, self).perform_update(serializer)
