from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completd, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled')
]
