from django.test import TestCase
from accounts.models import User, Profiles
from ..models import Post
from datetime import datetime
class TestPostModel(TestCase):
    def setUp(self):
        # U must be uppercase in setUp or else it won;t work
        self.user = User.objects.create_user(email="test@test.com", password='a/@1234567')
        self.profile = Profiles.objects.create(
            user = self.user,
            first_name = "test_first_name",
            last_name = "test_last_name",
            discription = "test discription",
        )
    def test_post_model(self):
        post = Post.objects.create(
            author = self.profile,
            title = "test",
            content = "test content",
            status = False,
            category = None,
            published_date = datetime.now(),
        )
        self.assertEqual(post.title, "test")