from django.conf import settings
from store.models import Product
from decimal import Decimal

class Cart:

    def __init__(self, request):
        # Store a reference to the current user's session object
        # so other Cart methods can access the session without
        # needing request.session every time.
        self.session = request.session 
        cart = self.session.get(settings.SESSION_CART_ID) # Retrieve the cart data stored under the session key. e.g. session["cart"]
        if not cart: # if key doesn't not exits
            cart = self.session[settings.SESSION_CART_ID] = {} # assigning empty dict to cart key. settings.SESSION_CART_ID = 'cart'
        self.cart = cart # making cart as instance attribute so that we can access in later methods


    def add(self, product,quantity=1, override_quantity=False):
        # Convert product ID to string because session data is serialized
        # and cart dictionary keys are stored as strings.
        product_id = str(product.id) # session data is converted into JSON and JSON want string for keys
        if product_id not in self.cart:
            self.cart[product_id]={"quantity":0,"price":str(product.price)} # because price is decimal class field

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity # Replace the existing quantity with the new quantity.
        else:
            self.cart[product_id]['quantity'] += quantity # # Add the new quantity to the existing quantity.
        self.save()

    def remove(self, product):
        """
        remove specific product from cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()


    def __iter__(self):
        """
        Iterates over the cart items and adds full product details to each.
        Flow:
        Template run loop (for item in cart)--> __iter__ trigger auto --> fetch cart data from session --> 
        fetch products from db matching with cart data --> make products dict {'1':<Product>} -->
        loop on every cart item --> product not found skip --> product found --> attach price, total price,
        product object --> yield(return 1 item at a time,pauses until next item is requested) -->
        goes to template --> user see full detail of cart like name,image, price etc.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        products_by_id = { str(product.id):product for product in products}
        for product_id, item_data in self.cart.items():
            product = products_by_id.get(product_id)
            if product is None:
                continue
            cart_item = item_data.copy()
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = (cart_item['price']*cart_item['quantity'])
            yield cart_item
        

    def __len__(self):
        """ 
        Returns the total number of items in the cart.
        e.g: iPhone (qty: 3) + Samsung (qty: 4) = 7 total items.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        calculate and return total price of all items
        e.g:iPhone (price:999*qt:4) + Samsung (price:499*qt:5)=Decimal(4999)
        """
        return sum(
            Decimal(item['price'])*item['quantity'] for item in self.cart.values()
        )
    
    def clear(self):
        """
        remove the whole cart from the current session
        """
        del self.session[settings.SESSION_CART_ID]
        self.save()

    # def update_quantity(self, product, quantity):
    #     """
    #     Update the quantity of the specific product
    #     e.g: update_quantity(iphone, 5)--> set iphone quantity to 5
    #     e.g: update_quantity(iphone,0)--> remove iphone from cart
    #     """
    #     product_id = str(product.id)
    #     if quantity <= 0:
    #         self.remove(product)
    #         return
    #     if product_id in self.cart:
    #         self.cart[product_id]['quantity'] = quantity
    #         self.save()


    def has_product(self, product):
        # check whether a specific product exits in cart
        return str(product.id) in self.cart
    
    def get_product_quantity(self, product):
        # get single product current quantity
        product_id = str(product.id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity'] 
        return 0
    
    def save(self):
        self.session.modified = True