from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

"""
Inline: add page inside another page
TabularInline: show OrderItem fields in tabular form
"""
class OrderItemInline(admin.TabularInline):
    
    model = OrderItem # use this model fields and show at admin page (In Tabular Form )
    raw_id_fields = ['product'] # Product dropdown ki jaga search popup dikhyga(product search krny k lye).Fast look up , easy to search.





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        'created',
        'updated',
        ]

    list_filter = ['paid','created','updated']
# Inside OrderAdmin page insert OrderItemInline page too.OrderItem fields should have shown in the same page as order item
    inlines = [OrderItemInline]