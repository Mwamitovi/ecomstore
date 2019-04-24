# cart/views.py
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from cart import cart
from utils import context_processors


def show_cart(request, template_name):
    cart_item_count = cart.cart_item_count(request)
    page_title = 'Shopping Cart'
    # return render_to_response(
    #     template_name, locals(), RequestContext(request)
    # )
    return render(
        request,
        template_name,
        {'cart_item_count': cart_item_count, 'page_title': page_title, },
        RequestContext(request, processors=[context_processors])
    )
