# cart/urls.py
from django.conf.urls import url
from cart import views


urlpatterns = [
    url(r'^$', views.show_cart,
        {'template_name': 'cart/cart.html'}, name='show_cart'
        ),
]