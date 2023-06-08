from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    UserSerializer,
    UserSerializer1,
    LoginSerializer,
    Otpserializer,
    BlogSerializer,
    BlogSerialize_wa,
)
from rest_framework.response import Response
from rest_framework import status
from .emails import send_otp
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Blogs

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

Users = get_user_model()


# Verify the otp
class otpview(APIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def check(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

    def get(self, request):
        self.check(request)
        if request.user.is_otp_verified:
            return Response("Your otp is already verified")
        return Response("Verify the user")

    def post(self, request):
        if request.user.is_otp_verified:
            return Response("Your otp is already verified")
        self.check(request)

        user = request.user
        set_otp = user.otp
        otp = Otpserializer(data=request.data)
        otp.is_valid(raise_exception=True)
        if set_otp == otp.validated_data["otp"]:
            user.is_otp_verified
            return Response({"detail": "Otp verified"}, status=200)
        else:
            return Response({"detail": "Otp invalid"}, status=400)


# For login view
class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response("You are already logged in!", status=400)
        return Response("Please pass your email and password to login", status=400)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            user = Users.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"detail": "User Does not exist"}, status=400)

        password_matches = user.check_password(password)
        if password_matches == False:
            return Response({"detail": "Invalid Credentials"}, status=400)

        authenticated_user = authenticate(
            request=request, email=email, password=password
        )

        if authenticated_user is None:
            return Response({"detail": "Authentication failed"}, status=400)
        login(request, authenticated_user)

        if user.is_otp_verified:
            return Response({"detail": "Login successful"}, status=200)
        else:
            return redirect(reverse("otp"))


# This is useful when a user forgets he is logged in but forgets otp
class sendotpagain(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        send_otp(request.user.email)
        return Response("Otp has been send on your mail address!")


# class ForgotPassword(APIView):


# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response("You are logged out")


# For user creation view
class UserCreateView(viewsets.ModelViewSet):
    # authentication_classes = []
    # permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserSerializer1

    def list(self, request):
        if request.user.is_authenticated:
            return Response({"details": "You are already logged in"})
        return Response("Please fill the form!")

    def create(self, request):
        if request.user.is_authenticated:
            return Response({"details": "You are already logged in"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        send_otp(serializer.validated_data.get("email"))
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Your account has been created. Check your email to verify and activate your account!",
            "data": serializer.data,
        }
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


# Create your views here.
# class UserCreateView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


# Blogging pagination
class BlogPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 4


# ALL blog By email


class BlogView(APIView):
    pagination_class = BlogPagination

    def get(self, request):
        paginator = self.pagination_class()

        blogs_query = Blogs.objects.all()
        paginated_blogs = paginator.paginate_queryset(blogs_query, request)
        blog_serializer = BlogSerialize_wa(paginated_blogs, many=True)
        # blog_serializer = BlogSerializer(blogs_query, many=True)
        # return Response(blog_serializer.data)
        return paginator.get_paginated_response(blog_serializer.data)


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    pagination_class = BlogPagination


class TestViewset1(APIView):
    pagination_class = BlogPagination

    def get(self, request):
        paginator = self.pagination_class()

        blogs_query = Users.objects.all()
        paginated_blogs = paginator.paginate_queryset(blogs_query, request)
        # blog_serializer = BlogSerializer(paginated_blogs, many=True)
        blog_serializer = UserSerializer(paginated_blogs, many=True)
        # return Response(blog_serializer.data)
        return paginator.get_paginated_response(blog_serializer.data)


# All BLog Randomly

# class BlogView(APIView):
#     pagination_class = BlogPagination

#     def get(self, request):
#         # paginator = self.pagination_class()


#         blogs_query = Blogs.objects.all()
#         # paginated_blogs = paginator.paginate_queryset(blogs_query, request)
#         # blog_serializer = BlogSerializer(paginated_blogs, many=True)
#         blog_serializer = BlogSerializer(blogs_query, many=True)
#         return Response(blog_serializer.data)
#         # return paginator.get_paginated_response(blog_serializer.data)
