from django.conf import settings
from django.core.mail import send_mail


def send_price_alert(url, price, desired_price):
    """
    Send email to user with given price and desired price.
    :param url: URL of the product in the email.
    :param price: price of the product in the email.
    :param desired_price: desired price specified by the user.
    :return: None.
    """

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
