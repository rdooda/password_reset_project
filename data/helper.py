from django.core.mail import send_mail
from django.conf import settings
import uuid


def send_forget_password(email, token):
    try:
        subject = "your forget password link"
        message = f'hi, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, 'otheremail@email.com']
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        print('a')
    except Exception as e:
        print(e)
    return True

