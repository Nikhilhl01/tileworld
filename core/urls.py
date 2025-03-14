from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_post, name='blog_post'),
    path('contact/', views.contact, name='contact'),
]