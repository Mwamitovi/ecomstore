# catalog/views.py
import json
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from ecomstore.settings import PRODUCTS_PER_ROW
from catalog.models import Category, Product, ProductReview
from catalog.forms import ProductAddToCartForm, ProductReviewForm
from utils import context_processors
from cart import cart
from stats import stats

import tagging
from tagging.models import Tag, TaggedItem
from tagging.utils import LOGARITHMIC


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
    p = get_object_or_404(Product, slug=product_slug)
    # categories = p.categories.all()
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
    # product review handling
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()

    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )


@login_required
def add_review(request):
    """ AJAX view that takes a form POST from a user submitting a new product review,
        requires a valid product slug and args from an instance of ProductReviewForm,
        returns a JSON response containing two variables:
        - review: contains a rendered template of the product review to update the product page,
        - success: a True/False value indicating if the save was successful.
    """
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        _slug = request.POST.get('slug')
        _product = Product.active.get(slug='_slug')
        review.user = request.user
        review.product = _product
        review.save()

        template = "catalog/product_review.html"
        html = render_to_string(template, {'review': review})
        response = json.dumps({'success': 'True', 'html': html})
    else:
        html = form.errors.as_ul()
        response = json.dumps({'success': 'False', 'html': html})
    return HttpResponse(
        response,
        content_type='application/javascript; charset=utf-8'
    )


@login_required
def add_tag(request):
    """ AJAX view that takes a form POST containing variables for a new product tag;
        requires a valid product 'slug' and comma-delimited tag list;
        returns a JSON response containing two variables:
        - success: indicates the status of save operation, and
        - tag: contains rendered HTML of all product pages for updating the product page.
    """
    tags = request.POST.get('tag', '')
    _slug = request.POST.get('slug', '')
    if len(tags) > 2:
        p = Product.active.get(slug=_slug)
        html = u''
        template = "catalog/tag_link.html"
        for _tag in tags.split():
            _tag.strip(',')
            Tag.objects.add_tag(p, _tag)
        for _tag in p.tags:
            html += render_to_string(template, {'tag': _tag})
        response = json.dumps({'success': 'True', 'html': html})
    else:
        response = json.dumps({'success': 'False'})
    return HttpResponse(
        response,
        content_type='application/javascript; charset=utf-8'
    )


def tag_cloud(request, template_name):
    """ contains a list of tags for active products,
        sized proportionately by relative frequency
    """
    product_tags = Tag.objects.cloud_for_model(
        Product,
        steps=9,
        distribution=LOGARITHMIC,
        filters={'is_active': True}
    )
    page_title = 'Product Tag Cloud'
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )


def tag(request, _tag, template_name):
    """ lists products which have been tagged with a given tag """
    products = TaggedItem.objects.get_by_model(Product.active, _tag)
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
