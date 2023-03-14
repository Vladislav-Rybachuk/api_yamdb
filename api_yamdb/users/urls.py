from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import sign_up_user, get_jwt_token, UserViewSet
from api.views import (CommentViewSet, ReviewViewSet,
                       CategoryViewSet, GenreViewSet, TitleViewSet)


app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('genres', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='category')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('auth/signup/', sign_up_user),
    path('auth/token/', get_jwt_token),
    path('', include(router.urls)),
]
