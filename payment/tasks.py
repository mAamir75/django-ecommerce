from celery import shared_task
from orders.models import Order
from django.core.mail import EmailMessage
from utils import generate_invoice_pdf


@shared_task
def payment_completed(order_id):

    order = Order.objects.get(id=order_id)
    email = EmailMessage(
        f"My Shop - Invoice no. {order.id}",
        "Please find attached your invoice.",
        None,
        [order.email],
    )


    pdf = generate_invoice_pdf(order)
    email.attach(
        f"order_{order.id}.pdf",
        pdf,
        "application/pdf",
    )
    email.send()