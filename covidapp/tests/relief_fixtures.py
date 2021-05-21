import pytest

from relief.models import State, RequestHelp

@pytest.fixture
def example_state():
    """Create a sample state model instance"""
    return State.objects.create(
        name='Sample state',
        slug='samplestate'
    )


@pytest.fixture
def example_help():
    """Create a sample help request"""
    return RequestHelp.objects.create(
        display_name='some name',
        mobile_number=12345,
        email='someemail@gmail.com',
        description='some help description',
        city='some city',
        address='some address',
        help_needed='oxygen'
    )
