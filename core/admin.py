from django.contrib import admin
from .models import Service, Project, Testimonial, BlogPost, Contact, SliderImage, BrandPartner

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
    list_display = ('name', 'email', 'phone', 'subject', 'status', 'email_sent', 'created_at')
    list_filter = ('status', 'email_sent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message', 'admin_notes')
    readonly_fields = ('email_sent', 'email_sent_at', 'created_at')
    list_editable = ('status',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'admin_notes', 'email_sent', 'email_sent_at', 'created_at')
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.email_sent:
            from django.core.mail import send_mail
            from django.conf import settings
            from django.template.loader import render_to_string
            
            # Send auto-response email to the user
            subject = f'Thank you for contacting TileWorld - {obj.subject}'
            message = f"Dear {obj.name},\n\nThank you for contacting TileWorld. We have received your inquiry and will get back to you shortly.\n\nBest regards,\nTileWorld Team"
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
                obj.mark_email_sent()
            except Exception as e:
                self.message_user(request, f'Error sending email: {str(e)}', level='ERROR')
        
        super().save_model(request, obj, form, change)


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'caption')
    ordering = ('order',)

@admin.register(BrandPartner)
class BrandPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'website', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('order',)
