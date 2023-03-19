from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Q

from .models import User
import re


class SignUpUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(allow_blank=False,
                                   max_length=254,
                                   required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=User.ROLES,
                                   default=User.ROLES[1][0],
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

        query = Q(email=data.get('email')) & Q(username=data.get('username'))
        if User.objects.filter(query).exists():
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
