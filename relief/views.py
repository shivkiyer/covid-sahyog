from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import utils
from .models import State, RequestHelp
from .forms import RequestHelpForm

# Create your views here.

def launch_app(request):
    context = {}
    context['list_of_states'] = State.objects.all()
    return render(request, 'index.html', context)


def request_help(request):
    context = utils.create_help_request_form()
    return render(request, 'request_help.html', context)


def offer_help(request):
    return render(request, 'offer_help.html', {})


def about_us(request):
    return render(request, 'about_us.html', {})


def submit_help_request(request):
    request_form = RequestHelpForm(request.POST)
    if request_form.is_valid():
        new_help_request = request_form.save()
    else:
        context = utils.create_help_request_form(request)
        return render(request, 'request_help.html', context)

    return redirect('confirm_submission')


def confirm_help(request):
    return render(request, 'confirmation.html', {})


def state_list(request, slug):
    context = {}
    state_chosen = State.objects.get(slug=slug)
    context['state'] = state_chosen
    help_in_state = state_chosen.requesthelp_set.all().order_by('-created_on')
    context['help_in_state'] = help_in_state
    return render(request, 'state_list.html', context)


# Method to create states.
def populate_db(request):
    State.objects.all().delete()
    list_of_states = utils.read_states()
    for state_item in list_of_states:
        if state_item:
            state_slug = ''.join(state_item.lower().split())
            State.objects.create(name=state_item, slug=state_slug)
    return HttpResponse('Populated')
