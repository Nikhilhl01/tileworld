from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Logo model for managing the website's logo
class Logo(models.Model):
    # Main logo image with recommended dimensions
    image = models.ImageField(upload_to='logo/', help_text='Recommended size: 150x50 pixels')
    # Flag to determine if this logo is currently active
    is_active = models.BooleanField(default=True)
    # Timestamps for creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'

    def save(self, *args, **kwargs):
        # Ensure only one logo is active at a time
        # Deactivate all other logos when setting a new one as active
        if self.is_active:
            Logo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Logo {self.id} ({"Active" if self.is_active else "Inactive"})'

# Service model for showcasing company services
class Service(models.Model):
    # Service title and detailed description
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Font Awesome icon for visual representation
    icon = models.CharField(max_length=50, help_text='Font Awesome icon class')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Project model for displaying company's portfolio
class Project(models.Model):
    # Project details including title, content, and featured image
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='projects/')
    # Timestamps for tracking creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Testimonial model for customer reviews and feedback
class Testimonial(models.Model):
    # Customer information
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    content = models.TextField()
    # Optional customer image
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    # Rating from 1 to 5
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    # Control testimonial visibility
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.position}'

# BlogPost model for managing company's blog content
class BlogPost(models.Model):
    # Blog post content and metadata
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    # Use timezone.now for flexible datetime handling
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # Control post visibility
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Contact model for storing contact form submissions
class Contact(models.Model):
    # Contact form fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, default='Project Inquiry')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Email tracking fields
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('archived', 'Archived')
        ],
        default='new'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Form Submission'
        verbose_name_plural = 'Contact Form Submissions'

    def __str__(self):
        return f'{self.name} - {self.subject} ({self.status})'

    def mark_email_sent(self):
        from django.utils import timezone
        self.email_sent = True
        self.email_sent_at = timezone.now()
        self.save()

# SliderImage model for managing homepage slider/carousel
class SliderImage(models.Model):
    # Slider image details
    title = models.CharField(max_length=200)
    # Image field with file extension validation
    image = models.ImageField(
        upload_to='slider/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    # Optional caption for the image
    caption = models.CharField(max_length=200, blank=True)
    # Control the order of images in the slider
    order = models.IntegerField(default=0)
    # Control image visibility
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order slider images by their specified order
        ordering = ['order']

    def __str__(self):
        return self.title

# BrandPartner model for managing partner logos in the sliding section
class BrandPartner(models.Model):
    # Partner name and logo image
    name = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='partners/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text='Recommended size: 200x100 pixels. Use transparent background if possible.'
    )
    # Website URL for the partner (optional)
    website = models.URLField(blank=True, null=True, help_text='Optional link to partner website')
    # Control the order of partners in the slider
    order = models.IntegerField(default=0)
    # Control partner visibility
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order partners by their specified order
        ordering = ['order']
        verbose_name = 'Brand Partner'
        verbose_name_plural = 'Brand Partners'

    def __str__(self):
        return self.name

# GalleryImage model for managing gallery images
class GalleryImage(models.Model):
    # Gallery image details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Image field with file extension validation
    image = models.ImageField(
        upload_to='gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    # Control the order of images in the gallery
    order = models.IntegerField(default=0)
    # Control image visibility
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title
