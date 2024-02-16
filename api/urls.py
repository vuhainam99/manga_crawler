from django.urls import path, include
from rest_framework import routers
from api.controllers import *
from api.views import CreateUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'ip_restriction', IPRestrictionViewSet, basename='ip_restriction')
router.register(r'crawl', CrawlLinkViewSet, basename='crawl')

urlpatterns = [
    path('', include(router.urls), name='api_index'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]