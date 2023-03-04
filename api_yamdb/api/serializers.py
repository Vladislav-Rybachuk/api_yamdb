from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Title, Review 
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    title_id = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        source='title',
        write_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    text = serializers.CharField()
    score = serializers.IntegerField(min_value=1, max_value=10)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'title', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Пользователь может оставить'
                        'только один отзыв на произведение'
            )
        ]

    def create(self, validated_data):
        title = validated_data.pop('title_id')
        review = Review.objects.create(title=title, **validated_data)
        return review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')
