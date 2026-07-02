from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from store.models import Product
from .forms import AddProductQuantityForm
from django.contrib import messages
# Create your views here.


@require_POST
def cart_add(request, product_id):
    
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductQuantityForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product = product,
            quantity = cd['quantity'],
            override_quantity = cd['override']
        )
        messages.success(request, f"Added {cd['quantity']}x {product.name} to your cart!")
    else:
        messages.error(request,"Invalid")
    return redirect('cart:cart_detail')
    

@require_POST
def cart_remove(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request,f"Cart item({product.name}) removed successfully!")
    return redirect('cart:cart_detail')
    



def cart_detail(request):
    
    cart = Cart(request)
    cart_items = []
    for item in cart:
        item['update_quantity_form'] = AddProductQuantityForm(
            initial={'quantity':item['quantity'], 'override':True}
        )
        cart_items.append(item)
    return render(request, 'cart/cart_detail.html', {'cart':cart, 'cart_items':cart_items})
