from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreationForm
from .models import OrderItem
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
            return render(request, 'orders/order_created.html', {'order':order})
    
    else:
        form = OrderCreationForm()
        return render(request, 'orders/order_create.html', {'cart':cart, 'form':form})
    