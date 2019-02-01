from .cart import Cart


def cart_middleware(get_response):
    """ request に cart を付与するミドルウェア
    """
    def middleware(request):
        cart_items = request.session.get('cart')
        if cart_items:
            cart = Cart.from_json(cart_items)
        else:
            cart = Cart()
        request.cart = cart

        response = get_response(request)

        if request.cart.edited:
            request.session['cart'] = request.cart.as_json()
        return response
    return middleware
