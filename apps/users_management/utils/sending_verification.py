from backend import settings
from backend.utils.email_queue_manager import email_queue_overhauler
from backend.utils.text_choices import EmailPriorityStatus, VerificationForStatus


def send_verification_email_otp(email_verification):
    otp = email_verification.otp
    subject = "Registration Confirmation"
    from_email = settings.EMAIL_HOST_USER
    if email_verification.using_for == VerificationForStatus.EMAIL_VERIFICATION:
        subject = "Email Verification"
        message = f"Your email verification OTP is: {otp}."
    elif email_verification.using_for == VerificationForStatus.PASSWORD_RESET:
        subject = "Password Reset"
        message = f"Your password reset OTP is: {otp}."

    else:
        message = f"Your OTP is: {otp}."
    email_queue_overhauler(
        subject=subject,
        body=message,
        to_email=email_verification.user.email,
        priority=EmailPriorityStatus.HIGH,
        context=None,
    )
    return otp
