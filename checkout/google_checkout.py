# checkout/google_checkout.py
from xml.dom.minidom import Document
from xml.dom import minidom
from django.http import HttpRequest, HttpResponseRedirect
import urllib
from urllib.request import Request, urlopen, HTTPError, URLError
import base64

from cart.models import CartItem
from cart import cart
from ecomstore import settings


def get_checkout_url(request):
    """ makes a request to Google Checkout with an XML cart,
    and parses out the returned checkout URL to which we send the customer
    when they are ready to check out.
    """
    redirect_url = ''
    req = _create_google_checkout_request(request)
    try:
        response_xml = urlopen(req).read()
    except HTTPError as err:
        raise err
    except URLError as err:
        raise err
        raise err
    else:
        redirect_url = _parse_google_checkout_response(response_xml)
    return redirect_url
































