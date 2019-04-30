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
    else:
        redirect_url = _parse_google_checkout_response(response_xml)
    return redirect_url


def _create_google_checkout_request(request):
    """ constructs a network request containing an XML version of a
    customer's shopping cart contents to submit to Google Checkout
    """
    url = settings.GOOGLE_CHECKOUT_URL
    cart = _build_xml_shopping_cart(request)
    req = Request(url=url, data=cart)
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID
    merchant_key = settings.GOOGLE_CHECKOUT_MERCHANT_KEY
    key_id = merchant_id + ':' + merchant_key
    authorization_value = base64.encodebytes(key_id)[:-1]
    req.add_header('Authorization', 'Basic %s' % authorization_value)
    req.add_header('Content-type', 'application/xml; charset=UTF-8')
    req.add_header('Accept', 'application/xml; charset=UTF-8')
    return req


def _parse_google_checkout_response(response_xml):
    """ get the XML response from an XML POST to Google Checkout
    of our shopping cart items """
    redirect_url = ''
    xml_doc = minidom.parseString(response_xml)
    root = xml_doc.domentElement
    node = root.childNodes[1]
    if node.tagName == 'redirect-url':
        redirect_url = node.firstChild.data
    if node.tagName == 'error-message':
        raise RuntimeError(node.firstChild.data)
    return redirect_url




























