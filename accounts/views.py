# accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from utils import context_processors


def register(request, template_name):
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
                url = urlresolvers.reverse('accounts:my_account')
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

















