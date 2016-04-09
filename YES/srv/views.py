from django.shortcuts import render
from django.http import HttpResponse

from .models import User, Resa

# Create your views here.
def index(request):
    context=None
    return render(request, 'srv/index.html', context)
