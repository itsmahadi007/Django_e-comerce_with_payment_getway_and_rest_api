import datetime
import random

from django.utils import timezone
from rest_framework import status

from apps.users_management.models import EmailVerification
from apps.users_management.utils.sending_verification import send_verification_email_otp
from backend.utils.text_choices import (
    VerificationForStatus,
)


def email_otp_process_before_sent(user, using_for):
    # this will process the phone verification before sending it, after processing it will shoot the mail
    message = ""
    if using_for == VerificationForStatus.EMAIL_VERIFICATION:
        message = f"Email verification OTP sent successfully."
    elif using_for == VerificationForStatus.PASSWORD_RESET:
        message = f"Password reset OTP sent successfully."

    try:
        email_verification = EmailVerification.objects.get(user=user)
        time_diff = timezone.now() - email_verification.created_at
        if (
            email_verification.used
            or timezone.now() > email_verification.expires_at
            or time_diff > datetime.timedelta(minutes=1)
        ):
            email_verification.expires_at = timezone.now() + datetime.timedelta(days=1)
            email_verification.created_at = timezone.now()
            email_verification.used = False

            email_verification.otp = random.randint(1000, 9999)
            email_verification.expires_at = timezone.now() + datetime.timedelta(days=1)
            email_verification.using_for = using_for
            email_verification.save()
            send_verification_email_otp(email_verification)
            return "New " + message
        else:
            send_verification_email_otp(email_verification)
            return message

    except EmailVerification.DoesNotExist:
        email_verification = EmailVerification(user=user)
        email_verification.otp = random.randint(1000, 9999)
        email_verification.expires_at = timezone.now() + datetime.timedelta(days=1)
        email_verification.using_for = using_for
        email_verification.save()
        send_verification_email_otp(email_verification)
        return "New " + message
    except Exception as e:
        print(e)
        return "Something went wrong" + str(e)


def email_otp_verification(
    user,
    otp,
    using_for,
    password=None,
    request=None,
):
    try:
        email_verification = EmailVerification.objects.get(user=user)
        if email_verification.using_for != using_for:
            print(email_verification.using_for, using_for)
            return "This OTP type is not Correct.", status.HTTP_400_BAD_REQUEST

        if email_verification.used:
            return "This OTP has already been used.", status.HTTP_400_BAD_REQUEST

        print(email_verification.otp, otp)
        if int(email_verification.otp) == int(otp):
            if timezone.now() <= email_verification.expires_at:
                message = "Email verified successfully."
                return_status = status.HTTP_200_OK
                if using_for == VerificationForStatus.EMAIL_VERIFICATION:
                    user.email_verified = True
                    user.save()
                elif using_for == VerificationForStatus.PASSWORD_RESET:
                    user.set_password(raw_password=password)
                    user.save()
                    message = "Password reset successfully."

                email_verification.used = True
                email_verification.save()
                return message, return_status
            else:
                return "OTP has expired.", status.HTTP_400_BAD_REQUEST
        else:
            return "Invalid OTP.", status.HTTP_400_BAD_REQUEST

    except EmailVerification.DoesNotExist:
        return "Email verification record not found.", status.HTTP_400_BAD_REQUEST
