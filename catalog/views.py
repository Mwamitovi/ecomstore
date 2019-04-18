# catalog/views.py
from django.shortcuts import get_object_or_404, render_to_response
from catalog.models import Category, Product
from django.template import RequestContext


def index(request, template_name='catalog/index.html'):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    return render_to_response(
        template_name, locals(), RequestContext(request)
    )
