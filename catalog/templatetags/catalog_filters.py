# templatetags/catalog_filters.py
from django import template
import locale

register = template.Library()


@register.filter(name='currency')
def currency(value):
    return '$' + str(value)

