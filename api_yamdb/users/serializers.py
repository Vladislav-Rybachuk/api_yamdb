from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, ROLES


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


class GetJwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    confirmation_code = serializers.CharField(required=True)


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
