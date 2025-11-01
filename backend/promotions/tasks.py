from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from products.models import Product
from orders.models import OrderItem
from whatsapp.utils import send_whatsapp_message

ADMIN_PHONE_NUMBER = "whatsapp:+254750979233"  # Replace with admin's WhatsApp number

@shared_task
def send_daily_product_summary():
    # Get new products from the last 24 hours
    new_products = Product.objects.filter(created_at__gte=timezone.now() - timedelta(days=1))

    # Get top 3 popular products in the last 30 days
    popular_products = (
        OrderItem.objects.filter(order__created_at__gte=timezone.now() - timedelta(days=30))
        .values("product__name")
        .annotate(total_sold=Count("id"))
        .order_by("-total_sold")[:3]
    )

    # --- Format the message ---
    message = "*📈 Daily Product Summary*\n\n"

    if new_products:
        message += "*✨ New Products:*\n"
        for product in new_products:
            message += f"- {product.name} (KES {product.price})\n"
    else:
        message += "No new products in the last 24 hours.\n"

    message += "\n*🔥 Popular Products (Last 30 Days):*\n"
    if popular_products:
        for i, item in enumerate(popular_products, 1):
            message += f"{i}. {item['product__name']} ({item['total_sold']} sold)\n"
    else:
        message += "No sales data in the last 30 days.\n"

    # --- Send the message ---
    if ADMIN_PHONE_NUMBER and ADMIN_PHONE_NUMBER != "whatsapp:":
        try:
            send_whatsapp_message(ADMIN_PHONE_NUMBER, message)
            return f"Sent daily summary to {ADMIN_PHONE_NUMBER}"
        except Exception as e:
            return f"Error sending message: {e}"
    else:
        return "Admin phone number not set. Message not sent."
