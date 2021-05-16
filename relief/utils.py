from django.conf import settings
from django.core.mail import send_mail

import os

from .models import State, RequestHelp
from .forms import RequestHelpForm

def read_states():
    """
    Reads the list of states from state.txt file in data directory.
    Returns - List of strings.
    """
    file_path = os.path.join(settings.BASE_DIR, 'data', 'states.txt')
    file_obj = open(file_path, 'r')
    state_list = [state.strip() for state in file_obj if len(state.strip())>0]
    print(state_list)

    return state_list


def create_help_form(request=None):
    """
    Creates either a blank help request form or a form with errors.
    Returns - context data with list of state, choices and RequestHelpForm
    """
    context = {}
    if request:
        context['request_form'] = RequestHelpForm(request.POST)
    else:
        context['request_form'] = RequestHelpForm()
    context['list_of_states'] = State.objects.all().order_by('name')
    context['help_choices'] = RequestHelp.help_choices
    return context


def create_email(help_obj, request):
    email_contents = help_obj.validation_email(request)
    send_mail(
        email_contents['subject'],
        email_contents['message'],
        settings.EMAIL_HOST_USER,
        email_contents['recipients'],
        fail_silently = False
    )
    return
