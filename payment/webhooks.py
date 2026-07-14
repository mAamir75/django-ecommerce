from django.conf import settings
import stripe
from django.http import HttpResponse
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from .tasks import payment_completed



@csrf_exempt
def stripe_webhook(request):
    
    payload = request.body
    sig_header = request.headers['STRIPE-SIGNATURE']
    key = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, key)
    
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if ( session.mode == 'payment' and session.payment_status == 'paid'):
            try:
                order = Order.objects.get(id = session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)
    return HttpResponse(status=200)
            


   
