from rest_framework import serializers

class SignUpUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    email = serializers.EmailField(allow_blank=False, required=True)
    first_name = serializers.CharField(max_length=256, required=False)
    last_name = serializers.CharField(max_length=256, required=False)
    role = serializers.CharField(max_length=256,
                                 default='user',
                                 required=False,
                                 write_only=True)
    bio = serializers.CharField(max_length=256, required=False)



class GetJwtTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    confirmation_code = serializers.CharField(required=True)