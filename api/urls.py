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
    path("send", views.sendotpagain.as_view(), name="again"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("blogs", views.BlogView.as_view(), name="blogs"),
    path("test1", views.TestViewset1.as_view(), name="blogs1"),
    # path("test", views.UserCreateView1.as_view(), name="create_user1"),
    # path("test", views.test.as_view(), name="user-create"),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
