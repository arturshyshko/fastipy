from django.urls import include, path
from rest_framework import routers

from .views import (
    healthcheck,
    login_user_via_email_password,
    logout_user,
    register_user_via_email_password,
)

router = routers.DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path("auth/register", register_user_via_email_password),
    path("auth/login", login_user_via_email_password),
    path("auth/logout", logout_user),
    path("healthcheck", healthcheck),
]
