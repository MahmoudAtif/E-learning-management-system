from django.conf import settings
from django.core.mail import send_mail


def send_registration_message(email):
    subject = 'Skola Registration'
    message = 'Thank you for Registration'
    email_from = settings.EMAIL_HOST
    send_mail(
        subject, message, email_from, [email]
    )
