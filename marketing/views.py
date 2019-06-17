# marketing/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from catalog.models import Product
from ecomstore.settings import BASE_DIR
import os
from utils import context_processors


ROBOTS_PATH = os.path.join(BASE_DIR, 'marketing/robots.txt')


def robots(request):
    """ view for robots.txt file """
    return HttpResponse(open(ROBOTS_PATH).read(), "text/plain")


def google_base(request):
    """ view for Google Base Product feed template; returns XML response """
    products = Product.active.all()
    template = get_template("marketing/google_base.xml")
    xml = template.render(
        request,
        locals(),
        RequestContext(request, processors=[context_processors])
    )
    return HttpResponse(xml, mimetype="text/xml")
