from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.db.models import Q

from datetime import datetime

from . import utils
from .models import State, RequestHelp
from .forms import RequestHelpForm

# Create your views here.

def launch_app(request):
    context = {}
    context['list_of_states'] = State.objects.all()
    return render(request, 'index.html', context)


def request_help(request):
    context = utils.create_help_form()
    return render(request, 'request_help.html', context)


def offer_help(request):
    context = utils.create_help_form()
    days = list(range(1, 32))
    months = list(range(1, 13))
    years = [2021, 2022]
    context['date_options'] = {
        'days': days,
        'months': months,
        'years': years
    }
    return render(request, 'offer_help.html', context)


def about_us(request):
    return render(request, 'about_us.html', {})


def submit_help_request(request):
    request_form = RequestHelpForm(request.POST)
    if request_form.is_valid():
        new_help_request = request_form.save(commit=False)
        start_day = request.POST.get('start_day')
        start_month = request.POST.get('start_month')
        start_year = request.POST.get('start_year')
        end_day = request.POST.get('end_day')
        end_month = request.POST.get('end_month')
        end_year = request.POST.get('end_year')
        start_date = datetime(
                int(start_year),
                int(start_month),
                int(start_day)
            )
        end_date = datetime(
                int(end_year),
                int(end_month),
                int(end_day)
            )
        new_help_request.start_date = start_date
        new_help_request.end_date = end_date
        new_help_request.is_help_offered = True
        new_help_request.save()
    else:
        context = utils.create_help_form(request)
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

@user_passes_test(lambda u: u.is_staff, login_url='/admin/')
def edit_help(request, help_id):
    context = {}
    help_obj = RequestHelp.objects.get(id=help_id)
    help_form = RequestHelpForm(instance=help_obj)
    context['help'] = help_obj
    context['request_form'] = help_form
    return render(request, 'help_validation.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='/admin/')
def validate_help(request, help_id):
    context = {}
    help_obj = RequestHelp.objects.get(id=help_id)
    if 'assistance_url' in request.POST:
        assistance_url = request.POST.get('assistance_url')
        help_obj.assistance_url = escape(assistance_url)
    if 'verified' in request.POST:
        if request.POST.get('verified') == 'on':
            help_obj.verified = True
    else:
        help_obj.verified = False
    if 'is_disabled' in request.POST:
        if request.POST.get('is_disabled') == 'on':
            help_obj.is_disabled = True
    else:
        help_obj.is_disabled = False

    help_obj.save()
    context['help_id'] = help_obj.id

    return render(request, 'validation_confirmation.html', context)


def logout_user(request):
    logout(request)
    return redirect('home_page')


def search_query(request):
    context = {}
    search_query = request.GET.get('search')
    search_logic = Q(help_needed__icontains=search_query)
    search_logic = search_logic | Q(display_name__icontains=search_query)
    search_logic = search_logic | Q(twitter_handle__icontains=search_query)
    search_logic = search_logic | Q(mobile_number__icontains=search_query)
    search_logic = search_logic | Q(email__icontains=search_query)
    search_logic = search_logic | Q(description__icontains=search_query)
    search_logic = search_logic | Q(address__icontains=search_query)
    search_logic = search_logic | Q(city__icontains=search_query)
    state = request.GET.get('state_id', '')
    if state:
        search_items = RequestHelp.objects.filter(
            state=state
        ).filter(search_logic)
    else:
        search_items = RequestHelp.objects.filter(search_logic)
    context['help_in_state'] = search_items
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
