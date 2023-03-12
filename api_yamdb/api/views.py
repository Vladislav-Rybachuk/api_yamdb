from django.db.models import Avg, PositiveSmallIntegerField
from django.shortcuts import get_object_or_404
from  rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Review, Title, Comment
from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdminModeratorAuthorPermission, IsAdminPermission
from .serializers import (CategorySerializer, GenreSerializer, 
                          TitleSerializer, ReviewSerializer, 
                          CommentSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminPermission,)

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
    permission_classes = (IsAdminPermission,)

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score', output_field=PositiveSmallIntegerField())
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminPermission, IsAuthenticatedOrReadOnly)

    
