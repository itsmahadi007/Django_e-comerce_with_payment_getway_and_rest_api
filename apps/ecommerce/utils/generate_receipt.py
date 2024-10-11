from django.template.loader import get_template
from weasyprint import HTML
from backend.utils.email_queue_manager import email_queue_overhauler
from backend.utils.text_choices import EmailPriorityStatus


def generate_receipt_for_cart(_confirmation_obj, context):
    html_template = get_template("PaymentSuccessPage.html")
    html_content = html_template.render(context)

    pdf = HTML(string=html_content).write_pdf()
    pdf_name = f"Receipt_transID_{_confirmation_obj.pg_txnid}_{_confirmation_obj.mer_txnid}.pdf"

    cart_obj = _confirmation_obj.payment_request.cart
    from django.core.files.base import ContentFile

    # print("Saving PDF")
    cart_obj.receipt.save(pdf_name, ContentFile(pdf), save=True)
    cart_obj.save()
    # print("PDF saved")

    email_queue_overhauler(
        subject="Payment Confirmation Receipt",
        body="Please find the attached receipt for your payment confirmation.",
        to_email=cart_obj.user.email,
        priority=EmailPriorityStatus.HIGH,
        context=None,
        attachment=cart_obj.receipt,
    )
