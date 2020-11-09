from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

SEX_CHOICE = [
    (1, "Nam"),
    (2, "Nữ"),
    (0, "Khác")
]


class MyUsers(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICE, default=1, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.FileField(upload_to='image/avatar', blank=True, null=True, default="avatar.jpg")


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        'my-email',
        [reset_password_token.user.email]
    )
