from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("test", views.UsersViewset, basename="test")
router.register("users", views.UserCreateView, basename="create_user")


urlpatterns = [
    path("", include(router.urls)),
    path("login", views.LoginView.as_view(), name="login"),
    path("otp", views.otpview.as_view(), name="otp"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
