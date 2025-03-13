from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Service, Project, Testimonial, BlogPost, Contact, SliderImage, Logo, BrandPartner

def home(request):
    services = Service.objects.all()[:3]
    projects = Project.objects.all()[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    logo = Logo.objects.filter(is_active=True).first()
    brand_partners = BrandPartner.objects.filter(is_active=True).order_by('order')
    return render(request, 'core/home.html', {
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'slider_images': slider_images,
        'logo': logo,
        'brand_partners': brand_partners
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})

def gallery(request):
    projects = Project.objects.all()
    return render(request, 'core/gallery.html', {'projects': projects})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'core/projects.html', {'projects': projects})

def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'core/blog.html', {'posts': posts})

def blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, is_published=True)
    return render(request, 'core/blog_post.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject', 'Project Inquiry')
        message = request.POST.get('message')
        
        # Save contact form submission
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Send auto-response email to user
        user_subject = f'Thank you for contacting TileWorld - {subject}'
        user_message = f"Dear {name},\n\nThank you for contacting TileWorld. We have received your inquiry and will get back to you shortly.\n\nBest regards,\nTileWorld Team"
        
        # Send notification email to admin
        admin_subject = f'New Contact Form Submission: {subject}'
        admin_message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}'
        
        try:
            # Send auto-response to user
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            # Send notification to admin
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            contact.mark_email_sent()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        
        return redirect('contact')
    
    return render(request, 'core/contact.html')
