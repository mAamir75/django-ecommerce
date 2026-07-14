from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import OrderCreationForm
from .models import OrderItem,Order
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from utils import generate_invoice_pdf
# Create your views here.





def create_order(request):

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
    
    else:
        form = OrderCreationForm()
        return render(request, 'orders/order_create.html', {'cart':cart, 'form':form})
    



@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render (
        request, 'admin/orders/order/detail.html', {'order':order}
    )




@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf = generate_invoice_pdf(order)
    response = HttpResponse(pdf, content_type = 'application/pdf')
    response['Content-Disposition'] = f"filename=order_{order.id}.pdf"
    return response
