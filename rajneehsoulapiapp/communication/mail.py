from tkinter import image_names

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rajneeshsoulapi import settings


def send_email(user):
    subject = "Welcome to TaskBreeze"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    print("user emailId : ", user.email)

    # Render HTML template with context
    html_content = render_to_string('email_template.html', {'user': user})

    # Create email
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")  # Attach HTML content

    # Send email
    email.send()


def send_email_anonymous(
    task_name,
    email,
    schedule_date_time,
    weatherStatus):
    subject = "Weather update on Task !!"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    task = f"""
    ✨ Task: {task_name}, on {schedule_date_time}
        
    \n--> Have eyes on mentioned Weather <--\n
    """

    image_url = "https://t4.ftcdn.net/jpg/02/66/38/15/360_F_266381525_alVrbw15u5EjhIpoqqa1eI5ghSf7hpz7.jpg"
    # Render HTML template with context
    html_content = render_to_string('email_template_weather_notify.html', {
        'email': email, "task": task, "image_url": image_url, "weatherStatus": weatherStatus})

    # Create email
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")  # Attach HTML content

    # Send email
    email.send()


def send_email_otp_verification(email, otp, valid_msg):
    subject = "Task Breeze Registration"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    # Render HTML template with context
    html_content = render_to_string('email_otp_verification_template.html', {'header_text': subject,
        'email': email, 'otp': otp, "validityPeriod": valid_msg})

    # Create email
    email = EmailMultiAlternatives(subject, "", from_email, to_email)
    email.attach_alternative(html_content, "text/html")  # Attach HTML content

    # Send email
    email.send()

