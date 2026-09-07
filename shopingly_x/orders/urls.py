from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    path('my-orders/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
