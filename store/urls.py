from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('',views.product_list,name='product-list'),
    path('<slug:category_slug>/', views.product_list, name='product-list-by-category'),
    path('<int:id>/<slug:category_slug>/', views.product_detail, name='product-detail'),
]
