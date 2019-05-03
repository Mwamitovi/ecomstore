# checkout/urls.py
from django.conf.urls import url
# from checkout import views
from ecomstore import settings


urlpatterns = [
    'checkout.views',
    url(r'^$', 'show_checkout',
        {'template_name': 'checkout/checkout.html', 'SSL': settings.ENABLE_SSL},
        name='checkout'
        ),
    url(r'^receipt/$', 'receipt',
        {'template_name': 'checkout/receipt.html', 'SSL': settings.ENABLE_SSL},
        name='checkout_receipt'
        ),
]
