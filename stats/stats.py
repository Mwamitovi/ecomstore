# stats/stats.py
import os
import base64
from search.models import SearchTerm
from ecomstore.settings import PRODUCTS_PER_ROW


def tracking_id(request):
    """ retrieve or generate a unique tracking ID in each user session
        to determine what pages a customer has viewed 
    """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']


def recommended_from_search(request):
    """ get the common words from the stored searches """
    common_words = frequent_search_words(request)
    from search import search
    matching = []
    for word in common_words:
        results = search.products(word).get('products', [])
        for r in results:
            if len(matching) < PRODUCTS_PER_ROW and r not in matching:
                matching.append(r)
    return matching

