from apps.ecommerce.models import ProductsModel
from apps.users_management.models import UserManage
from backend.utils.email_queue_manager import email_queue_overhauler
from backend.utils.text_choices import EmailPriorityStatus, UserType


def check_stock_and_notify_admins():
    low_stock_products = ProductsModel.objects.filter(stock__lt=5)

    if low_stock_products.exists():
        admin_emails = UserManage.objects.filter(user_type=UserType.ADMIN).values_list('email', flat=True)

        if admin_emails:
            product_details = "\n".join([
                f"Product: {product.name}, Stock: {product.stock}" for product in low_stock_products
            ])
            subject = "Low Stock Alert"
            body = f"The following products have low stock levels:\n\n{product_details}\n\nPlease take necessary action."

            email_queue_overhauler(
                subject=subject,
                body=body,
                to_email=list(admin_emails),
                priority=EmailPriorityStatus.HIGH,
                context=None,
                attachment=None,
            )
