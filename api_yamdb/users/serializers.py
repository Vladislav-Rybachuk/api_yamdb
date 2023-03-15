from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User
import re


ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

class SignUpUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(allow_blank=False,
                                   max_length=254,
                                   required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=ROLES,
                                   default='user',
                                   required=False,
                                   write_only=True)
    bio = serializers.CharField(required=False)

    def validate(self, data):
        if (re.match(r"^[\w.@+-]+\Z", data.get('username'))) is None:
            raise serializers.ValidationError(
                'Имя пользователя не соответствует шаблону')

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me')

        if (User.objects.filter(email=data.get('email')).exists()
                and User.objects.filter(
                username=data.get('username')).exists()):
            return data

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует')

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return data


class GetJwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me')

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует')

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return data
