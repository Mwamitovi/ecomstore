# utils/context_processors.py
from catalog.models import Category
from ecomstore import settings


def ecomstore(request):
    return {
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
