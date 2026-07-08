from django.shortcuts import render,get_object_or_404, redirect
import stripe
from django.conf import settings
from orders.models import Order
from django.urls import reverse
from decimal import Decimal
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY # stripe ko apni secret key de rhy taake wo humari request ko pehchan sky


def payment_process(request):

    order_id = request.session.get('order_id') # getting order id we defined in orders view, we saved this id in session
    order = get_object_or_404(Order, id=order_id)  # us id ka order database se le rhy, na mily to 404 error

    if request.method == 'POST':
        """
        After successfull payment go to this page or url
        build_absolute_uri: convert relative path(/payment/completed/) into
        absolute path (https://yoursite.com/payment/completed/)
        """
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # stripe checkout session banany k lye required data
        # mode, line_items, success_url are all stripe defined keys(built in) not django keys
        session_data = {
            'mode': 'payment', # one time payment
            'success_url':success_url, # payment completion k bd kaha jana
            'cancel_url': cancel_url,  # payment cancelation k bd kaha jana
            'client_reference_id': order.id, #  kn sy order ki payment kr rhy.stripe session order sy link ho jata ha
            'line_items': []  # products or price ki list ai gi
        }
        # Adding order item in stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data':{
                        'unit_amount':int(item.price * Decimal('100')),
                        'currency':'usd',
                        'product_data':{
                            'name':item.product.name,
                        },
                    },
                    'quantity':item.quantity,
                }
            )

        """
        checkout session bana rhy (ek temporary payment page jahan user apni
        card details fill kry ga)

        temporary kyun: man lo sirf 1 iphone bacha h, ek user payment page pe gya
        lekin din tak payment nahi ki. is dauran stripe samjhta h k ye buy krny wala h,
        is liye dusra koi user usy nahi khareed sakta.
        session temporary hony ki wja se, kuch time (jese 24 hours) k bad
        khud khatam ho jata h aur dusre users dobara try kr saktay hain
        """
        session = stripe.checkout.Session.create(**session_data) 
        return redirect(session.url, code = 303) # stripe created this session.url to redirect to payment page
        #code=303 isliye taake POST request GET mein convert ho k redirect ho
    else:
        """
        locals() function saary local variables (order, order_id, etc.) ko
        dictionary ki shakal mein return krta h
        render need request, html, context. this locals() is our context which contain like
        {'order':order, 'order_id':order.id,}
        """
        return render(request, 'payment/process.html', locals()) # locals() return dict of local variables like order, order_id






def payment_completd(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request,'payment/canceled.html')