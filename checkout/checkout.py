# checkout/checkout.py
from django.core.urlresolvers import reverse
import urllib
from cart import cart
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm
from checkout import authnet
from ecomstore import settings


# noinspection PyUnusedLocal
def get_checkout_url(request):
    """ returns the URL from the checkout module for cart """

    # use this for our own-site checkout
    return reverse('checkout')


def process(request):
    """ Takes a POST request containing valid order data;
    pings the payment gateway with the billing information and
    returns a Python dictionary with two entries: 'order_number' and 'message'
    based on the success of the payment processing.

    An unsuccessful billing will have an order_number of 0 and an error message,
    and a successful billing with have an order number and an empty string message.
    """

    # Transaction results
    _APPROVED = '1'
    _DECLINED = '2'
    _ERROR = '3'
    _HELD_FOR_REVIEW = '4'
    
    postdata = request.POST.copy()
    card_num = postdata.get('credit_card_number', '')
    exp_month = postdata.get('credit_card_expire_month', '')
    exp_year = postdata.get('credit_card_expire_year', '')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv', '')
    amount = cart.cart_subtotal(request)
    results = {}
    response = authnet.do_auth_capture(
        amount=amount,
        card_num=card_num,
        exp_date=exp_date,
        card_cvv=cvv
    )

    if response[0] == _APPROVED:
        transaction_id = response[6]
        order = create_order(request, transaction_id)
        results = {
            'order_number': order.id,
            'message': ''
        }
    if response[0] == _DECLINED:
        results = {
            'order_number': 0,
            'message': 'There is a problem with your Credit Card.'
        }
    if response[0] == _ERROR or response[0] == _HELD_FOR_REVIEW:
        results = {
            'order_number': 0,
            'message': 'Error processing your order.'
        }
    return results



































