from django.db import models
from django.conf import settings
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# Create your models here.


class Order(models.Model):

    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=200, blank=True)


    class Meta:
        
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):

        return f"Order {self.id}"

    def get_total_cost(self):
        # Get all OrderItems belonging to this order
        #items is the reference of OrderItem.
        # so self.items.all() is a reverse relation lookup that returns all OrderItem objects for this order
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    

    def get_stripe_url(self):

        if not self.stripe_id:

            return ''
        
        if '_test_' in settings.STRIPE_SECRET_KEY:

            path = '/test/'
        
        else:
            path = '/'
        
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())    

    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount/Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # 'store.Product' = alag app ka model, string se diya
    # direct import nahi -> circular error sy bachne ke liye
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='order_items')
    # Save the price at purchase time; future product price changes won't affect this order    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=1)


    

    def __str__(self):

        return str(self.id)
    
    def get_cost(self):
    # get cost of this single order item
        return self.price * self.quantity