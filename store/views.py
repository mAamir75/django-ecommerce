from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import AddProductQuantityForm
# Create your views here.


def product_list(request, category_slug=None):
# category=None q chaye reason:
# Category SELECT ki   →  if chala  →  category assign hua  →  koi error nahi
# agr category=None na ho:
# Category SELECT NI --> if nahi chala --> category kbhi bani hi ni jo context ma dy, agr category ha hi ni or context ma dy to  --> crash
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_for_sale = True)

    if category_slug:

        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        "category":category,
        "categories":categories,
        "products":products
    }

    return render(request, "store/product_list.html", context)


def product_detail(request, id, category_slug):

    product = get_object_or_404(Product, id=id, slug=category_slug, is_for_sale = True)
    cart_product_form = AddProductQuantityForm()
    return render(request, "store/product_detail.html", {"product":product, "cart_product_form":cart_product_form})

