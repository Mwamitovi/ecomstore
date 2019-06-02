# stats/stats.py
import os
import base64
from search.models import SearchTerm
from ecomstore.settings import PRODUCTS_PER_ROW
from catalog.models import Product
from stats.models import ProductView


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


def log_product_view(request, product):
    """ log the current customer as having viewed the given product instance """
    t_id = tracking_id(request)
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.ip_address = request.META.get('REMOTE_ADDR')
        v.tracking_id = t_id
        v.user = None
        if request.user.is_authenticated():
            v.user = request.user
        v.save()


def recommended_from_views(request):
    """ Pick product recommendations based on products the customer viewed;
        we get a list of tracking-IDs of other customers who also
        viewed the same products in the current customer's viewed products,
        and pick products which those other customers also viewed.
    """
    # get the recently viewed products
    viewed = get_recently_viewed(request)
    # if there are any previously viewed products,
    # get other tracking-ids that have viewed these same products
    if viewed:
        # note that .values() returns a QuerySet that returns dictionaries,
        # rather than model instances, when used as an iterable.
        products_viewed = ProductView.objects.filter(product__in=viewed).values('tracking_id')
        t_ids = [v['tracking_id'] for v in products_viewed]
        # if there are other tracking-ids, get those products
        if t_ids:
            all_viewed = Product.active.filter(products_viewed__tracking_id__in=t_ids)
            # if there are other products, get them, but exclude
            # any products that the customer has already seen/viewed
            if all_viewed:
                other_viewed = ProductView.objects.filter(
                    product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    return Product.active.filter(products_viewed__in=other_viewed).distinct()


def get_recently_viewed(request):
    """ get settings.PRODUCTS_PER_ROW most recently viewed products for current customer """
    t_id = tracking_id(request)
    views = ProductView.objects.filter(
        tracking_id=t_id).values('product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.active.filter(id__in=product_ids)





























