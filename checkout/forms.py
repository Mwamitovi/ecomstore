# checkout/forms.py
from django import forms
from checkout.models import Order
import datetime
import re


def cc_expire_years():
    """ list of years starting with current twelve years into the future """
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year + 12)
    return [
        (str(x), str(x)) for x in years
    ]


def cc_expire_months():
    """ list of tuples containing months of the year for use in credit card form.
    [('01','January'), ('02','February'), ... ]
    """
    months = []
    for month in range(1, 13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        months.append((numeric, datetime.date(2019, month, 1).strftime('%B')))
    return months


CARD_TYPES = (
    ('Mastercard', 'Mastercard'),
    ('VISA', 'VISA'),
    ('AMEX', 'AMEX'),
    ('Discover', 'Discover'),
)









































