from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def sent_mail(
    subject=None,
    message=None,
    to_email=None,
    from_email=None,
    template=None,
    attachment=None,
):
    email_from = settings.EMAIL_HOST_USER

    if not all([subject, message, to_email]):
        print("Missing essential email parameters.")
        return False

    # Ensure to_email is a list
    if not isinstance(to_email, list):
        to_email = [to_email]

    try:
        # Load the email template

        # Create email
        msg = EmailMultiAlternatives(subject, "Text Content", email_from, to_email)
        msg.attach_alternative(message, "text/html")

        # Attach file if attachment_path is provided
        if attachment:
            msg.attach(attachment.name, attachment.read(), "application/pdf")

        # Send email
        msg.send()
        return True
    except Exception as e:
        print(e)
        print(f"Failed to send email: {e}")
        return False
