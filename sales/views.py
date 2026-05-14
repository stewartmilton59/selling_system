from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
import json

from .models import Category, Product, Customer, Order, OrderItem, Review, Wishlist
from .forms import UserRegistrationForm, CustomerProfileForm, CheckoutForm, ReviewForm, ContactForm
from .cart import Cart


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    new_arrivals = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'sales/home.html', context)


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Sort
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
        'sort': sort,
    }
    return render(request, 'sales/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    reviews = product.reviews.all()
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(
            user=request.user
        )
        user_review = reviews.filter(customer=customer).first()
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(
            user=request.user
        )
        in_wishlist = Wishlist.objects.filter(customer=customer, product=product).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.customer = request.user.customer
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', slug=slug)
    else:
        review_form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'sales/product_detail.html', context)


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'sales/categories.html', {'categories': categories})


# Cart Views
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'sales/cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items available in stock.')
        return redirect('product_detail', slug=product.slug)
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart!')
    return redirect('cart_detail')


def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items available.')
        return redirect('cart_detail')
    
    cart.update(product=product, quantity=quantity)
    return redirect('cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Cart cleared!')
    return redirect('cart_detail')


def get_or_create_customer(user):
    """Helper function to get or create customer for a user"""
    customer, created = Customer.objects.get_or_create(
        user=user
    )
    return customer


# Checkout Views
@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_detail')
    
    customer = get_or_create_customer(request.user)
    
    # Pre-fill with customer data if available
    initial_data = {}
    if customer.address:
        initial_data = {
            'shipping_name': f"{request.user.first_name} {request.user.last_name}",
            'shipping_phone': customer.phone,
            'shipping_address': customer.address,
            'shipping_city': customer.city,
            'shipping_state': customer.state,
            'shipping_zip': customer.zip_code,
        }
    
    # Calculate totals (needed for both GET and POST)
    subtotal = cart.get_total_price()
    shipping = Decimal('10.00') if subtotal < Decimal('100.00') else Decimal('0.00')
    tax = subtotal * Decimal('0.08')  # 8% tax
    total = subtotal + shipping + tax
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            
            # Use the already calculated values
            order.subtotal = subtotal
            order.shipping_cost = shipping
            order.tax = tax
            order.total = total
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    total=item['total_price']
                )
                # Update stock
                product = item['product']
                product.stock -= item['quantity']
                product.save()
            
            # Clear cart
            cart.clear()
            
            messages.success(request, f'Order placed successfully! Order ID: {order.order_id}')
            return redirect('order_confirmation', order_id=order.order_id)
    else:
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'sales/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    customer = get_or_create_customer(request.user)
    order = get_object_or_404(Order, order_id=order_id, customer=customer)
    return render(request, 'sales/order_confirmation.html', {'order': order})


# User Account Views
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'sales/register.html', {'form': form})


def logout_view(request):
    """Log out the user and redirect to home page."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    customer = get_or_create_customer(request.user)
    orders = customer.orders.all()[:10]
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer)
    
    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'sales/profile.html', context)


@login_required
def order_history(request):
    customer = get_or_create_customer(request.user)
    orders = customer.orders.all()
    return render(request, 'sales/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    customer = get_or_create_customer(request.user)
    order = get_object_or_404(Order, order_id=order_id, customer=customer)
    return render(request, 'sales/order_detail.html', {'order': order})


# Wishlist Views
@login_required
def wishlist(request):
    customer = get_or_create_customer(request.user)
    wishlist_items = Wishlist.objects.filter(customer=customer)
    return render(request, 'sales/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    customer = get_or_create_customer(request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        customer=customer,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect('product_detail', slug=product.slug)


@login_required
def remove_from_wishlist(request, product_id):
    customer = get_or_create_customer(request.user)
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(customer=customer, product=product).delete()
    messages.success(request, f'{product.name} removed from wishlist!')
    return redirect('wishlist')


# Dashboard View (for admin/staff)
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    # Sales statistics
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    
    # Recent orders
    recent_orders = Order.objects.all()[:10]
    
    # Top selling products
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('-total_sold')[:5]
    
    # Orders by status
    orders_by_status = Order.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'orders_by_status': orders_by_status,
    }
    return render(request, 'sales/dashboard.html', context)


# Contact Page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'sales/contact.html', {'form': form})


# About Page
def about(request):
    return render(request, 'sales/about.html')


# AJAX Views
def ajax_cart_count(request):
    cart = Cart(request)
    return JsonResponse({
        'count': len(cart),
        'total': str(cart.get_total_price())
    })


def ajax_add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        
        if quantity > product.stock:
            return JsonResponse({
                'success': False,
                'message': f'Sorry, only {product.stock} items available.'
            })
        
        cart.add(product=product, quantity=quantity)
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })
    return JsonResponse({'success': False, 'message': 'Invalid request'})
