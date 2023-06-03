from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer, UserSerializer1, LoginSerializer, Otpserializer
from rest_framework.response import Response
from rest_framework import status
from .emails import send_otp
from rest_framework.views import APIView

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib.auth import authenticate, login

Users = get_user_model()


class otpview(APIView):
    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def check(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

    def get(self, request):
        self.check(request)
        return Response("Verify the user")

    def post(self, request):
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

    # def dispatch(self, request, *args, **kwargs):
    #     print(request.user.is_authenticated)
    #     if not request.user.is_authenticated:
    #         return redirect(reverse("login"))


class LoginView(APIView):
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
            return Response({"detail": "Password is incorrect"}, status=400)

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


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserCreateView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer1

    def create(self, request):
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
