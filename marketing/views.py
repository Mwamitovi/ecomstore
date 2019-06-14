# marketing/views.py
from django.http import HttpResponse
from ecomstore.settings import BASE_DIR
import os


ROBOTS_PATH = os.path.join(BASE_DIR, 'marketing/robots.txt')


def robots(request):
    """ view for robots.txt file """
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')
