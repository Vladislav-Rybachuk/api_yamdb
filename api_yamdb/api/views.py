from django.db.models import Avg, PositiveSmallIntegerField
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from  rest_framework import filters, status, viewsets
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title
from .mixins import ListCreateDeleteViewSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer,)


class GenreVieSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    #permission_classes = (IsAdminPermission,)

    def retrieve(self, request, slug=None):
        if not Genre.objects.filter(slug=slug).count():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().retrieve(self, request, slug)
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    #permission_classes = (IsAdminPermission,)

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews_score', output_field=PositiveSmallIntegerField())
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    #permission_classes = ()

    