from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# from django.contrib.sites.shortcuts import get_current_site


@shared_task
def send_email_registeration(email):
    subject = "Skola Registeration Successfully"
    message = f"Thank you for yhour registeration discoover our courses"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [
            email,
        ],
    )
    print("success")


@shared_task
def send_registration_message(email):
    subject = "Skola Registration"
    message = "Thank you for Registration"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])


@shared_task
def test():
    return "hello"
