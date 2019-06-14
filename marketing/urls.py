# marketing/urls.py
from django.conf.urls import url
from marketing import views


urlpatterns = [
    url(r'^robots\.txt$', views.robots ),
]
