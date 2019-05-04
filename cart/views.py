# cart/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from cart import cart
from utils import context_processors
from checkout import checkout


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
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)

    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
