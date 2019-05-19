# search/templatetags/search_tags.py
from django import template
from search.forms import SearchForm
import urllib


register = template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    q = request.GET.get('q', '')
    form = SearchForm({'q': q})
    return {'form': form}
