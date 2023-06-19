from rest_framework import serializers
from api.models import Blogs


class UserBlog(serializers.ModelSerializer):
    email = serializers.EmailField(source="staff_member")

    # profile_picture = serializers.SerializerMethodField()

    # active = serializers.BooleanField(source="is_active")
    class Meta:
        model = Blogs

        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ["date", "blog_title", "blog_content", "staff_member"]
