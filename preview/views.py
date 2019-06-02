# preview/views.py
from django.shortcuts import render


def home(request):
    # return render_to_response("index.html")
    return render(request, "index.html")
