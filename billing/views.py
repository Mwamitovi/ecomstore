# billing/views.py
import json
from django.shortcuts import render
from django.core import serializers
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from utils import context_processors

from billing.forms import CardForm
from billing import passkey         # expected after skipped sections


@login_required
def add_card(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # convert the POST variables into ``json`` format
        post_data.__delitem__('csrfmiddlewaretoken')
        json_data = json.dumps(post_data)
        # encrypt the json
        encrypted_json = passkey.encrypt(json_data)
        # retrieve the encrypted json
        decrypted_json = passkey.decrypt(encrypted_json)
        # convert the decrypted json into a dict
        decrypted_data = json.loads(decrypted_json)

        # store the newly encrypted data aa a Cad instance
        form = CardForm(post_data)
        card = form.save(commit=False)
        card.user = request.user
        card.num = post_data.get('card_number')[-4:]
        card.data = encrypted_json
        card.save()
    else:
        form = CardForm()

    return render(
        request,
        "billing/add_card.html",
        locals(),
        RequestContext(request, processors=[context_processors])
    )
