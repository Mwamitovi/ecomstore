# checkout/views.py
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from checkout import checkout
from cart import cart
from utils import context_processors


def show_checkout(request, template_name):
    """ checkout form page to collect user shipping and billing information """
    if cart.is_empty(request):
        cart_url = reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)

    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = reverse('checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Please correct the errors below'
    else:
        form = CheckoutForm()
    page_title = 'Checkout'

    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )























