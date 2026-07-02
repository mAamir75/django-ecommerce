from django.db import models
from utils import generate_unique_slug
from django.urls import reverse


class Category(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    class Meta:
        
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]


    def save(self, *args, **kwargs):

        if not self.slug:
           
           self.slug = generate_unique_slug(Category, self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        # Flow: Page Render → Method Call → URL Build → Link Ready → User Click → View Handles
        # Request → View → DB → Template → get_absolute_url() → reverse() → URL Generated → User Click → URL Match → View → Response
        return reverse("store:product-list-by-category", args=[self.slug])
    
    
class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_for_sale = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        
    def save(self, *args, **kwargs):

        if not self.slug:
            
            self.slug = generate_unique_slug(Product, self.name)
           
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
# Flow: Page Render → Method Call → URL Build → Link Ready → User Click → View Handles
        return reverse("store:product-detail", args=[self.id, self.slug])
    

