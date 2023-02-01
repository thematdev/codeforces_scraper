import click
import os
from click_shell import shell
from codeforces_scraper import Scraper
from termforces.session_manager import load_session

SEARCH_LOCATIONS = ['.', '..', os.path.join(os.path.expanduser('~'), '.config', 'termforces')]
FILE_NAME = 'termforces_cookies.json'


class State:
    def __init__(self):
        self.scraper = Scraper()


def preload_session(state):
    for loc in SEARCH_LOCATIONS:
        file_path = os.path.join(loc, FILE_NAME)
        if os.path.exists(file_path):
            print(f'Loading session from {file_path}')
            load_session(state.scraper, file_path)
            return


@shell(prompt='termforces > ', intro='Entering termforces shell')
@click.pass_context
def termforces_shell(ctx):
    state = State()
    preload_session(state)
    ctx.obj = state
    pass
