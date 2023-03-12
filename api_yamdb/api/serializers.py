from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title


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
        