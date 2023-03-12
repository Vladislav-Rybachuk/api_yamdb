from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


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

 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title 
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        
        def validate_year(self, value):
            current_year = timezone.now().year
            if 0 < value > current_year:
                raise serializers.ValidationError(
                    'Произведение не может быть из будущего')
            return value
          

