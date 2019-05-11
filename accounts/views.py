# accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from utils import context_processors
from checkout.models import Order, OrderItem


def register(request, template_name):
    """ view displaying customer registration form """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username', '')
            pw = postdata.get('password', '')

            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = reverse('accounts:my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )


@login_required()
def my_account(request, template_name):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )


@login_required()
def order_details(request, order_id, template_name):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )












