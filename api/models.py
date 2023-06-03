from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings


class UsersManager(BaseUserManager):
    def create_user(self, email, username, password=None, **other_fields):
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **other_fields,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_otp_verified", True)

        user = self.create_user(
            email=email,
            password=password,
            username=username,
            **other_fields,
        )
        if user.is_staff is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if user.is_superuser is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        user.save(using=self._db)
        return user


# Create your models here.
class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20)
    otp = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=20, unique=True, default=None)
    email = models.EmailField(primary_key=True)
    profile_picture = models.ImageField(null=True, upload_to="photos", blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_otp_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UsersManager()

    def __str__(self) -> str:
        return f"{self.name}{self.email}"


class Blogs(models.Model):
    date = models.DateField(auto_now=True)
    blog_title = models.CharField(max_length=20, primary_key=True)
    blog_content = models.CharField(max_length=10000)
    staff_member = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="Blogs", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.blog_title}"
