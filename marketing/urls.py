# marketing/urls.py
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from marketing import views
from marketing.sitemaps import SITEMAPS


urlpatterns = [
    url(r'^robots\.txt$', views.robots),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}),
    url(r'^google_base\.xml$', views.google_base),
]
