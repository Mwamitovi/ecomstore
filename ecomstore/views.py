# ecomstore/views.py
from django.shortcuts import render_to_response
from django.template import RequestContext


def file_not_found_404(request):
    page_title = 'Page Not Found'
    return render_to_response(
        '404.html', locals(), RequestContext(request)
    )
