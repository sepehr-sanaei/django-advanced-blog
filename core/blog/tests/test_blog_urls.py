from django.test import TestCase
from django.urls import reverse, resolve
from ..views import IndexView, PostListView
# Create your tests here.
class TestURL(TestCase):
    
    def test_blog_url_index_resolve(self):
        url = reverse('blog:index')
        self.assertEqual(resolve(url).func.view_class, IndexView)