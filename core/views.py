from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Service, Project, Testimonial, BlogPost, Contact

def home(request):
    services = Service.objects.all()[:3]
    projects = Project.objects.all()[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    return render(request, 'core/home.html', {
        'services': services,
        'projects': projects,
        'testimonials': testimonials,
        'blog_posts': blog_posts
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
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save contact form submission
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification
        email_message = f'Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}'
        try:
            send_mail(
                subject=f'New Contact Form Submission: {subject}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        
        return redirect('contact')
    
    return render(request, 'core/contact.html')
