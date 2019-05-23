# search/urls.py
from django.conf.urls import url
from search import views


urlpatterns = [
    url(r'^results/$', views.results,
        {'template_name': 'search/results.html'},
        name='search_results'
        ),
]