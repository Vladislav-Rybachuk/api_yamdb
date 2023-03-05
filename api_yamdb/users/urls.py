from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from users.views import sign_up_user, get_jwt_token, UserViewSet



app_name = 'users'

router = DefaultRouter()
# Вызываем метод .register с нужными параметрами
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', sign_up_user),
    path('auth/token/', get_jwt_token),
    path('', include(router.urls)),
]