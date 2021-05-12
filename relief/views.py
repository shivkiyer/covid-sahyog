from django.shortcuts import render
from django.http import HttpResponse

from . import utils
from .models import State

# Create your views here.

def launch_app(request):
    context = {}
    context['list_of_states'] = State.objects.all()
    return render(request, 'index.html', context)


def request_help(request):
    return render(request, 'request_help.html', {})


def offer_help(request):
    return render(request, 'offer_help.html', {})


def about_us(request):
    return render(request, 'about_us.html', {})


def populate_db(request):
    list_of_states = utils.read_states()
    for state_item in list_of_states:
        if state_item:
            State.objects.create(name=state_item)
    return HttpResponse('Populated')
