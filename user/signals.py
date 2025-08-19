from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Student
from app.models import Author
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_student_or_instructor(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(student=instance, name=instance.username)
        elif instance.is_instructor:
            Author.objects.create(
                author=instance,
                name=instance.username,
            )
            Student.objects.create(
                Student=instance,
                name=instance.username,
            )


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    message = "{}?token={}".format(
        instance.request.build_absolute_uri(
            reverse("password_reset:reset-password-confirm")
        ),
        reset_password_token.key,
    )
    send_mail(
        "Sent Token To Reset Password",
        message,
        settings.EMAIL_HOST_USER,
        [
            reset_password_token.user.email,
        ],
    )
