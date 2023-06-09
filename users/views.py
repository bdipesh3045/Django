from rest_framework.views import APIView
from api.models import Blogs
from rest_framework.permissions import IsAuthenticated
from api.views import BlogPagination
from django.contrib.auth import get_user_model
from .serializers import UserBlog, BlogSerializer
from api.serializers import User_detail
from rest_framework.response import Response
from rest_framework import status


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


class Users(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email

        Users = get_user_model()
        user_details = Users.objects.filter(pk=email)

        data = User_detail(user_details, many=True)

        return Response(data={"Details": data.data}, status=status.HTTP_200_OK)


class BlogCrud(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = BlogPagination

    def get(self, request, blog_title=None):
        if blog_title is not None:
            try:
                blog = Blogs.objects.get(
                    staff_member__email=request.user.email, blog_title=blog_title
                )
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Blogs.DoesNotExist:
                return Response(
                    {"Details": "Resource does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            paginator = self.pagination_class()
            email = request.user.email
            blogs = Blogs.objects.filter(staff_member__email=email)
            paginated_blogs = paginator.paginate_queryset(blogs, request)
            SerializedData = UserBlog(paginated_blogs, many=True)
            return paginator.get_paginated_response(SerializedData.data)

    def post(self, request):
        request.data["staff_member"] = request.user
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_title=None):
        try:
            blog = Blogs.objects.get(
                staff_member__email=request.user.email, blog_title=blog_title
            )
            blog.delete()
            return Response(
                {"Details": "Blog deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Blogs.DoesNotExist:
            return Response(
                {"Details": "Resource does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    # def put(self, request, blog_title=None):
    #     try:
    #         blog = Blogs.objects.get(
    #             staff_member__email=request.user.email, blog_title=blog_title
    #         )
    #         serializer = BlogSerializer(blog, data=request.data)

    #         if serializer.is_valid():
    #             serializer.validated_data["blog_title"] = blog_title
    #             serializer.save()
    #             return Response(
    #                 {"Details": "Blog Data Updated", "Data": serializer.data},
    #                 status=status.HTTP_201_CREATED,
    #             )

    #     except Blogs.DoesNotExist:
    #         return Response(
    #             {"Details": "Resource does not exist"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    # def patch(self, request, blog_title=None):
    #     try:
    #         blog = Blogs.objects.get(
    #             staff_member__email=request.user.email, blog_title=blog_title
    #         )
    #         serializer = BlogSerializer(blog, data=request.data, partial=True)

    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(
    #                 {"Details": "Blog Data Updated", "Data": serializer.data},
    #                 status=status.HTTP_201_CREATED,
    #             )

    #     except Blogs.DoesNotExist:
    #         return Response(
    #             {"Details": "Resource does not exist"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    def put(self, request, blog_title=None):
        try:
            blog = Blogs.objects.get(
                staff_member__email=request.user.email, blog_title=blog_title
            )
            request.data["staff_member"] = request.user
            serializer = BlogSerializer(blog, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"Details": "Blog Data Updated", "Data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response(
                {"Details": "Resource does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, blog_title=None):
        try:
            blog = Blogs.objects.get(
                staff_member__email=request.user.email, blog_title=blog_title
            )
            request.data["staff_member"] = request.user
            serializer = BlogSerializer(blog, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"Details": "Blog Data Updated", "Data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response(
                {"Details": "Resource does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
