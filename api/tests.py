from django.test import TestCase
from .models import Users, Blogs
from .serializers import BlogSerializer


class BlogSerializerTestCase(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            name="John Doe", email="john@example.com", profile_picture=None
        )
        self.blog = Blogs.objects.create(
            blog_title="Test Blog", blog_content="Test Content", staff_member=self.userc
        )

    def test_blog_serializer(self):
        serializer = BlogSerializer(instance=self.blog)
        print(serializer.data)
        # expected_data = {
        #     "name": "John Doe",
        #     "email": "john@example.com",
        #     "Blogs": ["Test Blog"],
        # }

        # self.assertEqual(serializer.data, expected_data)
