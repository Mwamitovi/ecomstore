# search/search.py
from search.models import SearchTerm
from catalog.models import Product
from django.db.models import Q


STRIP_WORDS = [
    'a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
    'of', 'on', 'or', 'that', 'the', 'to', 'with'
]


def store(request, q):
    """ store the search text in the database """
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        term.save()


def products(search_text):
    """ get products matching the search text """
    words = _prepare_words(search_text)
    _products = Product.active.all()
    results = {'products': []}
    # iterate through the keywords
    for word in words:
        _products = _products.filter(
            Q(name__icontains=word) |
            Q(description__icontains=word) |
            Q(sku__icontains=word) |
            Q(brand__icontains=word) |
            Q(meta_description__icontains=word) |
            Q(meta_keywords__icontains=word)
        )
        results['products'] = _products
    return results


def _prepare_words(search_text):
    """ strip out common words, limit to 5 words """
    _words = search_text.split()
    for common in STRIP_WORDS:
        if common in _words:
            _words.remove(common)
    return _words[0:5]
