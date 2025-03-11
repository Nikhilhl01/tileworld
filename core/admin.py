from django.contrib import admin
from .models import Service, Project, Testimonial, BlogPost, Contact, SliderImage

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'position', 'content')
    list_editable = ('is_active',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'caption')
    ordering = ('order',)
