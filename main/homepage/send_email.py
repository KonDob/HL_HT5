from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(recipient_list=None, activate_url=None):
    subject = 'Thank you for registering to our test site'
    message = 'Hello to world'
    email_from = settings.EMAIL_HOST_USER

    template = get_template('send_active_code.html')

    send_mail(subject=subject, message=message,
              recipient_list=recipient_list,
              from_email=email_from,
              html_message=template.render(
                  context={
                      "activate_url": activate_url,
                  }
              ))
