# accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from utils import context_processors
from checkout.models import Order, OrderItem
from accounts.forms import UserProfileForm, RegistrationForm
from accounts import profile


def register(request, template_name):
    """ view displaying customer registration form """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = RegistrationForm(postdata)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = postdata.get('email', '')
            user.save()
            un = postdata.get('username', '')
            pw = postdata.get('password', '')

            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = reverse('accounts:my_account')
                return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
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


@login_required()
def order_info(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            profile.set_(request)
            url = reverse('accounts:my_account')
            return HttpResponseRedirect(url)
    else:
        user_p = profile.retrieve(request)
        form = UserProfileForm(instance=user_p)
    page_title = 'Edit Order Information'
    return render(
        request,
        template_name,
        locals(),
        RequestContext(request, processors=[context_processors])
    )










