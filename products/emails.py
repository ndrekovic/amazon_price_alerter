from django.conf import settings
from django.core.mail import send_mail


def send_price_alert(url, price, desired_price):

    subject = "Price Alert 🚨"

    message = (
        f"Price Limit: {desired_price}€\n"
        f"Current Price: {price}€\n\n"
        f"{url}"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False
    )
    print("Email sent successfully.")
