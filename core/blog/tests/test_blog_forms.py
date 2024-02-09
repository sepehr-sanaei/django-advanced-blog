from django.test import TestCase
from ..forms import PostForm
from ..models import Category
from datetime import datetime
class TestForm(TestCase):
    
    def test_form_is_valid_data(self):
        category_obj = Category.objects.create(name="hello")
        form = PostForm(data={
            "title":"sepehr",
            "content":"zalmin",
            "status":False,
            "category":category_obj,
            "published_date":datetime.now()
            
        })
        self.assertTrue(form.is_valid())
        
    def test_form_with_no_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())