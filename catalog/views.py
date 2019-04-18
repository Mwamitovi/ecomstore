# catalog/views.py
from django.shortcuts import get_object_or_404, render_to_response
from catalog.models import Category, Product
from django.template import RequestContext


def index(request, template_name):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    context = RequestContext(request, )
    return render_to_response(
        template_name, locals(), RequestContext(request)
    )


def show_category(request, category_slug, template_name):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render_to_response(
        template_name, locals(), RequestContext(request)
    )


def show_product(request, product_slug, template_name):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    return render_to_response(
        template_name, locals(), RequestContext(request)
    )
