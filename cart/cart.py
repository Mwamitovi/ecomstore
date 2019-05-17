# cart/cart.py
from catalog.models import Product
from cart.models import CartItem
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from ecomstore import settings
import decimal
import random


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """ get the current user's cart id, sets new one if blank;
    Note: the syntax below matches the text, but an alternative,
    clearer way of checking for a cart ID would be the following:

    if not CART_ID_SESSION_KEY in request.session:
    """
    # if 'cart_id' in request.session:
    #     request.session['cart_id'] = _generate_cart_id()
    # return request.session['cart_id']
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """ function for generating random cart ID values """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRQSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


def get_cart_items(request):
    """ return all items from the current user's cart """
    return CartItem.objects.filter(cart_id=_cart_id(request))


def add_to_cart(request):
    """ function that takes a POST request and
    adds a product instance to the current customer's shopping cart
    """
    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
    product_slug = postdata.get('product_slug', '')
    # get quantity added, return 1 if empty
    quantity = postdata.get('quantity', 1)
    # fetch the product or return a missing page error
    p = get_object_or_404(Product, slug=product_slug)
    # get products in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True

    if not product_in_cart:
        # create and save a new cart item
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


def cart_distinct_item_count(request):
    """ returns the total number of items in the user's cart """
    return get_cart_items(request).count()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def update_cart(request):
    """ function takes a POST request that updates
    the quantity for single product instance in the current customer's shopping cart
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


def remove_from_cart(request):
    """ function that takes a POST request,
    and removes a single product instance from the current customer's shopping cart
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):
    """ gets the subtotal for the current shopping cart """
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    user_cart = get_cart_items(request)
    user_cart.delete()



















