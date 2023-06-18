from rest_framework.views import APIView
from api.models import Blogs
from rest_framework.permissions import IsAuthenticated
from api.views import BlogPagination
from django.contrib.auth import get_user_model
from .serializers import UserBlog

Users = get_user_model()


class UserBlogs(APIView):
    pagination_class = BlogPagination

    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = self.pagination_class()
        email = request.user.email
        blog = Blogs.objects.filter(staff_member__email=email)
        paginated_blogs = paginator.paginate_queryset(blog, request)
        SerializedData = UserBlog(paginated_blogs, many=True)
        return paginator.get_paginated_response(SerializedData.data)
