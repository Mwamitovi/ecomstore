# cart/views.py
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from cart import cart
from utils import context_processors


def show_cart(request, template_name):
    """ view function for the page displaying the customer shopping cart,
    and allows for the updating of quantities and removal of product instances
    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    # cart_item_count = cart.cart_distinct_item_count(request)
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
