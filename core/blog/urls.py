from django.urls import path
from django.views.generic import TemplateView, RedirectView
from . import views


app_name = 'blog'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('go-to-index', RedirectView.as_view(pattern_name="blog:index"), name="go-to-index"),
    path('post/', views.PostView.as_view(), name="post"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post-detail"),
    
]