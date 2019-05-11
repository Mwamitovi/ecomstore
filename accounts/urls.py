# accounts/urls.py
from django.conf.urls import url
from django.contrib.auth import views
from ecomstore import settings
import accounts.views


urlpatterns =[
    url(r'^register/$', accounts.views.register,
        {'template_name': 'registration/register.html', 'SSL': settings.ENABLE_SSL},
        name='register'
        ),
    url(r'^my_account/$', accounts.views.my_account,
        {'template_name': 'registration/my_account.html'},
        name='my_account'
        ),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', accounts.views.order_details,
        {'template_name': 'registration/order_details.html'},
        name='order_details'
        ),
]

urlpatterns += [
    url(r'^login/$', views.login,
        {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL},
        name='login'
        ),
]