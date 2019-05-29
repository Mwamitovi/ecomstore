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


def frequent_search_words(request):
    """ gets the highest-ranking 3 search words
        from the last 10 search terms the current customer has entered
    """
    # first, get the ten most recent searches from the database.
    searches = SearchTerm.objects.filter(
        tracking_id=tracking_id(request)
    ).values('q').order_by('-search_date')[0:10]
    # then, join all the search terms together into a single string
    search_string = ' '.join([search['q'] for search in searches])
    # and return the top 3 most common words in the search terms
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(some_string):
    """ takes a single string of space-delimited word, and
        returns a list of words they contain from most to least frequent
    """
    # first, let's convert string into a python list
    words = some_string.split()
    # then, we assign a rank to each word based on it's frequency
    ranked_words = [[word, words.count(word)] for word in set(words)]
    # and we sort the words based on descending (highest-to-lowest) frequency
    sorted_words = sorted(ranked_words, key=lambda word: -word[1])
    # then, we return the list of words, most frequent first
    return [p[0] for p in sorted_words]
