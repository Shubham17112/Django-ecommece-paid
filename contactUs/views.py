from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Prepare email content
            email_subject = f"Contact Form: {subject}" if subject else "New Contact Form Submission"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            
            # Send email
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Replace with your recipient email
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})