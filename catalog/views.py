# catalog/views.py
from django.shortcuts import get_object_or_404, render_to_response, render
from catalog.models import Category, Product
from django.template import RequestContext
from django.core import urlresolvers
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm
from utils import context_processors


def index(request, template_name):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    # return render_to_response(
    #     template_name, locals(), RequestContext(request, [context_processors])
    # )
    return render(
        request,
        template_name,
        {'page_title': page_title},
        RequestContext(request, processors=[context_processors])
    )


def show_category(request, category_slug, template_name):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    # return render_to_response(
    #     template_name, locals(), RequestContext(request)
    # )
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
    # return render_to_response(
    #     template_name, locals(), RequestContext(request)
    # )
    return render(
        request,
        template_name,
        {'categories': categories, 'page_title': page_title,
         'meta_keywords': meta_keywords, 'meta_description': meta_description,
         'form': form, 'cart': cart,
        },
        RequestContext(request, processors=[context_processors])
    )
