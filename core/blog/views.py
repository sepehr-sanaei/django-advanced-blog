from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post
# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['name'] = 'man intin'
        context['posts'] = Post.objects.all()
        return context
    
class PostView(ListView):
    # model = Post
    queryset = Post.objects.all()
    context_object_name = 'posts'
    ordering = '-id'
    
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts
    
    
class PostDetailView(DetailView):
    model = Post