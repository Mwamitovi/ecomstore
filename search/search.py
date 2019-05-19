# search/search.py
from search.models import SearchTerm
from catalog.models import Product
from django.db.models import Q


STRIP_WORDS = [
    'a','an','and','by','for','from','in','no','not',
    'of','on','or','that','the','to','with'
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






































