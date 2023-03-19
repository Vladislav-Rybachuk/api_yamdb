from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import SYSTEM_EMAIL
from .models import User
from .permissions import IsAdministator, AllowedForMe
from users.serializers import (GetJwtTokenSerializer, SignUpUserSerializer,
                               UserSerializer)


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
            current_user = User.objects.get(username=username, email=email)
        else:
            current_user = User.objects.create_user(username=username,
                                                    email=email)

        confirm_code = account_activation_token.make_token(current_user)
        send_mail('Confirmation of registration',
                  f'your code: {confirm_code}',
                  SYSTEM_EMAIL,
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

    @action(detail=False, methods=['get', 'delete', 'patch'], url_path='me')
    def me(self, request):

        if self.request.method == 'GET':
            serializer = self.get_serializer(self.request.user, many=False)
            return Response(serializer.data)

        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True)
            if serializer.is_valid():
                if (serializer.instance.role != self.request.data.get('role')):
                    serializer.save(role=serializer.instance.role)
                    return Response(serializer.data)
                else:
                    serializer.save()
                    super(UserViewSet, self).perform_update(serializer)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        if self.request.method == 'DELETE':
            raise MethodNotAllowed('DELETE')

    def get_object(self):
        username = self.kwargs.get('username')
        if self.request.method == 'PUT':
            raise MethodNotAllowed('PUT')

        current_user = get_object_or_404(User, username=username)
        return current_user

    def get_permissions(self):
        if self.action == 'me':
            return (AllowedForMe(), permissions.IsAuthenticated())

        return super().get_permissions()
