from django.urls import path
from .views import (
    home,
    add_to_cart,
    cart_view,
    increase_quantity,
    decrease_quantity,
    checkout,
    order_history,
    delete_product,
    payment,
    product_detail,
    add_review,
    
)

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('increase/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path(
    'delete-product/<int:product_id>/',
    delete_product,
    name='delete_product'
),
path(
    'payment/',
    payment,
    name='payment'
),
path(
    'product/<int:product_id>/',
    product_detail,
    name='product_detail'

),
path(
    'review/<int:product_id>/',
    add_review,
    name='add_review'
),
    
]