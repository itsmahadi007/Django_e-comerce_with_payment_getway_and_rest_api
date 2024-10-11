from django.template.loader import get_template
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from django.utils.timezone import make_aware
import datetime

from backend.utils.email_queue_manager import email_queue_overhauler
from backend.utils.text_choices import EmailPriorityStatus


def generate_receipt_for_cart(_confirmation_obj, context):
    try:
        # Make pay_time timezone-aware if it's naive
        pay_time = _confirmation_obj.pay_time
        if pay_time is not None and isinstance(pay_time, datetime.datetime) and pay_time.tzinfo is None:
            pay_time = make_aware(pay_time)
        context['pay_time'] = pay_time

        html_template = get_template("Payment_Success_Receipt.html")
        html_content = html_template.render(context)

        print("creating pdf")

        # Generate PDF using xhtml2pdf
        pdf_name = f"Receipt_transID_{_confirmation_obj.pg_txnid}_{_confirmation_obj.mer_txnid}.pdf"
        pdf_file = ContentFile(b"")  # Creating an empty file object to store PDF

        # Use pisa to convert HTML to PDF
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if not pisa_status.err:
            cart_obj = _confirmation_obj.payment_request.cart
            cart_obj.receipt.save(pdf_name, pdf_file, save=True)
            print("pdf saved")

            email_queue_overhauler(
                subject="Payment Confirmation Receipt",
                body="Please find the attached receipt for your payment confirmation.",
                to_email=cart_obj.user.email,
                priority=EmailPriorityStatus.HIGH,
                context=None,
                attachment=cart_obj.receipt,
            )
        else:
            # Log error or handle the case where PDF generation failed
            print("PDF generation failed. No PDF was created.")
    except Exception as e:
        # Handle or log the exception
        print(f"An error occurred: {e}")
