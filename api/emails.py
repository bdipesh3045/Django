from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import Users


def send_otp(email):
    otp = randint(0000, 9999)

    subject = "Your verification otp is given below:"
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user_obj = Users.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
