from rest_framework import serializers
from .models import Blogs, Users
import bleach


# class UserVerify(serializers.ModelSerializer):
#     class meta


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, write_only=True)
    email = serializers.EmailField()

    class Meta:
        fields = ["email", "password"]

    def validate(self, attrs):
        pw = attrs["password"]

        if len(pw) <= 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        if len(pw) > 15:
            return serializers.ValidationError(
                "Password exceeds the maximum length of 15"
            )
        if bleach.clean(pw) != pw:
            return serializers.ValidationError(
                "There is something html encoding attached to your pw Try removing it"
            )
        attrs["email"] = bleach.clean(attrs["email"])

        return attrs


# New code that works
# Importing Blog serializer
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ["date", "blog_title"]


class UserSerializer(serializers.ModelSerializer):
    latest_blog = serializers.SerializerMethodField()

    # Importing User serializer
    def get_latest_blog(self, user):
        latest_blog = Blogs.objects.filter(staff_member=user.email)
        # Custom logic to retrieve the latest blog for the user
        # latest_blog = Blogs.objects.filter(staff_member_id=user.email)
        Blog = BlogSerializer(latest_blog, many=True)
        return Blog.data

    class Meta:
        model = Users
        fields = ["name", "email", "latest_blog", "profile_picture"]


# Usercreate trial 1


class UserSerializer1(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ["name", "username", "password", "email", "profile_picture"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_password(self, pw):
        if len(pw) <= 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        if len(pw) > 15:
            return serializers.ValidationError(
                "Password exceeds the maximum length of 15"
            )
        if bleach.clean(pw) != pw:
            return serializers.ValidationError(
                "There is something html encoding attached to your pw Try removing it"
            )
        return pw

    # cleaning all the data before saving it into database
    def validate(self, attrs):
        attrs["name"] = bleach.clean(attrs["name"])
        attrs["username"] = bleach.clean(attrs["username"])
        attrs["email"] = bleach.clean(attrs["email"])
        return attrs

    # Image validation remaining
