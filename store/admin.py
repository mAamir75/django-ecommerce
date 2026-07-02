from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':['name']} # auto generate slug only in admin panel


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name']}
    list_display = ['image_preview', 'name','price','stock','is_for_sale', 'in_stock']
    list_display_links = ['image_preview','name']
    search_fields = ['name','category__name']
    list_filter = ['category','is_for_sale','created_at']
    list_editable = ['stock','is_for_sale']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    date_hierarchy = 'created_at' # show products or filter products by year/month/date. 
    actions = ['mark_available', 'mark_unavailable']
    
    fieldsets = [
        (
            'Product Info', {'fields':['category', 'image', 'image_preview', 'name','slug', 'description']}
        ),
        (
            'Price Info', {'fields':['price'],'classes':['collapse']}
        ),
        (
            'Inventory Info', {'fields':['stock','is_for_sale']}
        ),
        (
            'TimeStamp', {'fields': ['created_at','updated_at'],'classes':['collapse']}
        )
    ]

# without this only file.png show , using this proper image will show
# Renders a thumbnail,image in admin list view.
# format_html auto-escapes the image URL to prevent XSS attacks.
    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" /> ', obj.image.url)
        return "No image"


# jo products selected, mark ha wo sale k lye available ha
# Admin bulk action: Mark selected products as available for sale.
# Uses queryset.update() for fast bulk update (single SQL query).
    @admin.action(description="Mark selected products as available!")
    def mark_available(self,request, queryset):
        queryset.update(is_for_sale = True)

    @admin.action(description="Mark selected products as unavailable!")
    def mark_unavailable(self, request, queryset):
        queryset.update(is_for_sale=False)


# if product is > 0, show In shock. 
    @admin.display(boolean=True, description="In Stock")
    def in_stock(self, obj):
        return obj.stock>0