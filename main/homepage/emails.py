from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(title: str, description: str, recipients: list):

    email_from = settings.EMAIL_HOST_USER
    template = get_template('send_email_template.html')
    send_mail(subject=title, message=description, from_email=email_from,
              recipient_list=recipients,
              html_message=template.render(
                  context={
                      'recipients': recipients,
                  }
              ))
