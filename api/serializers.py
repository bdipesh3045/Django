from rest_framework import serializers
from .models import Blogs, Users
import bleach


# class UserVerify(serializers.ModelSerializer):
#     class meta
class Otpserializer(serializers.Serializer):
    otp = serializers.IntegerField(max_value=9999, min_value=0000)

    class Meta:
        fields = ["otp"]


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


# Serializers to show full blog data
# class Blogserializers(serializers.ModelField):
#     class Meta:
#         model = Blogs
#         fields = ["date", "blog_title", "blog_content", "staff_member"]


class User_detail(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = [
            # "email",
            # "is_staff",
            # "is_active",
            "is_superuser",
            # "is_otp_verified",
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "otp",
        ]


class BlogSerialize_wa(serializers.ModelSerializer):
    email = serializers.EmailField(source="staff_member")
    # data = serializers.SerializerMethodField()
    # data = UserBlog(source="staff_member")
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    # active = serializers.BooleanField(source="is_active")
    class Meta:
        model = Blogs

        fields = [
            # "data",
            "email",
            "name",
            "username",
            "profile_picture",
            "date",
            "blog_title",
            "blog_content",
        ]
        filterset_fields = ["date"]

    def get_username(self, obj):
        return obj.staff_member.username

        # data = obj["data"]
        # return data["username"]

    def get_name(self, obj):
        return obj.staff_member.name

    # return obj.data.name
    # data = obj["data"]
    # return data["name"]

    def get_profile_picture(self, obj):
        return (
            obj.staff_member.profile_picture.url
            if obj.staff_member.profile_picture
            else None
        )
        # return obj.staff_member.profile_picture

    # data = obj["data"]
    # return obj.data.profile_picture
    # return data["profile_picture"]

    # def get_data(self, blogs):
    #     user_data = Users.objects.filter(email=blogs.staff_member)
    #     print(user_data)
    #     # Custom logic to retrieve the latest blog for the user
    #     # latest_blog = Blogs.objects.filter(staff_member_id=user.email)
    #     user = UserBlog(user_data)
    #     return user.data
