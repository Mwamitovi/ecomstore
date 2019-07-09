# catalog/views.py
from django.shortcuts import get_object_or_404, render
from catalog.models import Category, Product
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.core.cache import cache

from cart import cart
from catalog.forms import ProductAddToCartForm
from utils import context_processors
from stats import stats
from ecomstore.settings import PRODUCTS_PER_ROW, CACHE_TIMEOUT


def index(request, template_name):
    """ site home page """
    search_recoms = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recoms = stats.recommended_from_views(request)
    page_title = 'Musical Instruments and Sheet Music for Musicians'

    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )


def show_category(request, category_slug, template_name):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description

    return render(
        request,
        template_name,
        {'products': products, 'page_title': page_title,
         'meta_keywords': meta_keywords, 'meta_description': meta_description,
         },
        RequestContext(request, processors=[context_processors])
    )


def show_product(request, product_slug, template_name):
    """ view for each product page, with POST vs GET detection """
    product_cache_key = request.path
    # get product from cache
    p = cache.get(product_cache_key)
    # if cache miss, fall back to db query
    if not p:
        p = get_object_or_404(Product.active, slug=product_slug)
        # store in cache for next time
        cache.set(product_cache_key, p, CACHE_TIMEOUT)

    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        # add to cart
        # Create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('cart:show_cart')
            return HttpResponseRedirect(url)
    else:
        # It's a GET, so create the unbound form,
        # And notice the request is passed as a keyword arg (kwargs)
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    # log current user as having seen/viewed this product instance
    # utilized in evaluating product recommendations
    stats.log_product_view(request, p)

    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
