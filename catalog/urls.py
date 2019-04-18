# catalog/urls.py
from django.conf.urls import url
from catalog import views


urlpatterns = [
    url(r'^$', index,
        {'template_name':'catalog/index.html'},
        name='catalog_home'
        ),
    url(r'^category/(?P<category_slug>[-\w]/$)', show_category,
        {'template_name':'catalog/category.html'},
        name='catalog_category'
        ),
    url(r'^product/(?P<product_slug>[-\w]+)/$', show_product,
        {'template_name':'catalog/product.html'},
        name='catalog_product'
        ),
]