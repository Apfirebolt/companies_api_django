from django.urls import path
from .views import (
    CreateCustomUserApiView,
    UserProfileApiView,
    ListCompaniesApiView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register", CreateCustomUserApiView.as_view(), name="signup"),
    path("login", TokenObtainPairView.as_view(), name="signin"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("profile", UserProfileApiView.as_view(), name="profile"),
    path("companies", ListCompaniesApiView.as_view(), name="companies"),
]
