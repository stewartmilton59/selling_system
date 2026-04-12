from .cart import Cart


def cart_processor(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart),
        'cart_total': cart.get_total_price(),
    }
