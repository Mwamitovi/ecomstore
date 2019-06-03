# search/views.py
from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from search import search
from ecomstore import settings
from utils import context_processors


def results(request, template_name):
    """ template for displaying settings.PRODUCTS_PER_PAGE
        paginated product results
    """
    # get current search phrase
    q = request.GET.get('q', '')
    # get current page number. Set to 1, if missing or is invalid
    try:
        _page = int(request.GET.get('page', 1))
    except ValueError:
        _page = 1
    # retrieve the matching products
    matching = search.products(q).get('products')
    # generate the paginator object
    paginator = Paginator(matching, settings.PRODUCTS_PER_PAGE)
    try:
        _results = paginator.page(_page).object_list
    except (InvalidPage, EmptyPage):
        _results = paginator.page(1).object_list
    # store the search
    search.store(request, q)
    page_title = 'Search Results for: ' + q
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
