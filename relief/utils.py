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


def create_help_form(request=None, is_help_offered=False):
    """
    Creates either a blank help request form or a form with errors.
    Returns - context data with list of state, choices and RequestHelpForm
    """
    context = {}
    if request:
        context['request_form'] = RequestHelpForm(request.POST)
    else:
        if is_help_offered:
            sample_offer = RequestHelp()
            sample_offer.is_help_offered = True
            context['request_form'] = RequestHelpForm(instance=sample_offer)
        else:
            context['request_form'] = RequestHelpForm()
    context['list_of_states'] = State.objects.all().order_by('name')
    context['help_choices'] = RequestHelp.help_choices
    days = [str(x) for x in range(1, 32)]
    months = [str(x) for x in range(1, 13)]
    years = ["2021", "2022"]
    context['date_options'] = {
        'days': days,
        'months': months,
        'years': years
    }
    return context


def create_email(help_obj, request):
    email_contents = help_obj.validation_email(request)
    volunteer_emails = [x.strip() for x in help_obj.volunteers.split(',')]
    email_contents['recipients'].extend(volunteer_emails)
    send_mail(
        email_contents['subject'],
        email_contents['message'],
        settings.EMAIL_HOST_USER,
        email_contents['recipients'],
        fail_silently = False
    )
    return
