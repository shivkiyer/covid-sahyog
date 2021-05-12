from django.conf import settings
import os

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
