from getpass import getpass

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_credentials():
    """Prompt for and return a username and password."""
    username = get_input('Enter Username: ')
    password = getpass()
    return username, password