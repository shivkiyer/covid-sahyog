import pytest

from relief.models import State, RequestHelp
from relief.forms import RequestHelpForm

from .relief_fixtures import example_state, example_help

@pytest.mark.django_db
def test_home(client, example_state):
    """Test the home page lists the states in database"""
    web_response = client.get('')
    assert web_response.status_code == 200
    assert 'Sample state' in str(web_response.content)


@pytest.mark.django_db
def test_state(client, example_state):
    """Detail view of a state should have no requests
    or offers in the beginning."""
    web_response = client.get('/state/samplestate')
    assert web_response.status_code == 200
    assert 'No requests or offers found' in str(web_response.content)


@pytest.mark.django_db
def test_help_request_form(example_state):
    """Filling a help request or offer form"""
    form_data = {}
    form_data['display_name'] = 'xyz'
    form_data['mobile_number'] = 'xyz'
    form_data['email'] = 'xyz'
    form_data['description'] = 'xyz'
    form_data['help_needed'] = 'food'
    form_data['state'] = example_state.id
    form_data['address'] = 'xyz'
    form_data['city'] = 'xyz'
    request_form = RequestHelpForm(data=form_data)

    # Form should not be valid because of invalid mobile and email
    assert request_form.is_valid() == False
    assert "Mobile number should only be digits." in request_form.errors['mobile_number']
    assert "Enter a valid email address." in request_form.errors['email']

    form_data['mobile_number'] = 12345
    request_form = RequestHelpForm(data=form_data)

    # Form should not be valid because of email
    assert request_form.is_valid() == False
    assert 'mobile_number' not in request_form.errors.keys()
    assert "Enter a valid email address." in request_form.errors['email']

    form_data['email'] = 'xyz@gmail.com'
    request_form = RequestHelpForm(data=form_data)

    # Form is now valid
    assert request_form.is_valid() == True


@pytest.mark.django_db
def test_view_request_in_state(client, example_state, example_help):
    """A help request associated with a state should
    be listed when a request is made to the state url."""
    example_help.state = example_state
    example_help.save()

    web_response = client.get('/state/samplestate')

    # Unverified requests or offers should not appear
    assert web_response.status_code == 200
    assert 'No requests or offers found' in str(web_response.content)

    example_help.verified = True
    example_help.save()

    web_response = client.get('/state/samplestate')

    # After verification, they will be displayed
    assert web_response.status_code == 200
    assert 'some name' in str(web_response.content)

    # Disabling a request or offer should hide it again.
    example_help.is_disabled = True
    example_help.save()

    web_response = client.get('/state/samplestate')

    assert web_response.status_code == 200
    assert 'No requests or offers found' in str(web_response.content)
