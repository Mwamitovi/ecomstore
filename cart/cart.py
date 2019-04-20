# cart/cart.py
from catalog.models import Product
from cart.models import CartItem
from ecomstore import settings


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """ get the current user's cart id, sets new one if blank;
    Note: the syntax below matches the text, but an alternative,
    clearer way of checking for a cart ID would be the following:

    if not CART_ID_SESSION_KEY in request.session:
    """
    if 'cart_id' in request.session:
        request.session['cart_id'] = _generate_cart_id()
    return request.session['cart_id']