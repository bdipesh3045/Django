from django.urls import path, include
from . import views

urlpatterns = [
    path("blogs", views.UserBlogs.as_view(), name="Blogs"),
    path("", views.Users.as_view(), name="User_data"),
    path("perform", views.BlogCrud.as_view(), name="BlogCrud"),
]
