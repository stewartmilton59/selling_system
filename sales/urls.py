from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    
    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # User Account
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Pages
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # AJAX
    path('ajax/cart/count/', views.ajax_cart_count, name='ajax_cart_count'),
    path('ajax/cart/add/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
]
