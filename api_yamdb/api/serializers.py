from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    
    
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        
        
    
    def validate (self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError
        return data


    
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


class TitleBaseSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title 
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlePostSerializer(serializers.ModelSerializer):
        genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                             queryset=Genre.objects.all()
                                             )
        category = serializers.SlugRelatedField(slug_field='slug',
                                                queryset=Category.objects.all()
                                                )
        
        class Meta:
            model = Title
            fields = ('id', 'name', 'year', 'description', 'genre', 'category')
            
        def validate_year(self, value):
            current_year = timezone.now().year
            if 0 < value > current_year:
                raise serializers.ValidationError(
                    'Произведение не может быть из будущего')
            return value
          

