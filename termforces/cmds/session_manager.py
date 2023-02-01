import click
import os
from termforces.termforces_shell import termforces_shell, State
from termforces.session_manager import load_session, store_session
from getpass import getpass
from codeforces_scraper import ScraperError


@termforces_shell.command()
@click.argument('handle')
@click.option('--password',
              help="Will be prompted, so do not pass, unless you're sure for safety")
@click.option('--session-file', help='Tries to store session on successful login')
@click.option('--no-getpass', is_flag=True,
              show_default=True, default=False, help='Read password from stdin instead of using getpass')
@click.pass_obj
def login(state: State, handle, password, session_file, no_getpass):
    if password is None:
        if no_getpass:
            password = input()
        else:
            password = getpass(f'Codeforces password for {handle}: ')
    try:
        state.scraper.login(handle, password)
    except ScraperError:
        print('Failed to login, check your credentials')
        return
    if session_file is not None:
        store_session(state.scraper, os.path.expanduser(session_file))


@termforces_shell.command(name='load-session')
@click.argument('session_file')
@click.pass_obj
def load_session_cmd(state: State, session_file):
    load_session(state.scraper, os.path.expanduser(session_file))


@termforces_shell.command(name='whoami')
@click.pass_obj
def whoami(state: State):
    state.scraper.update_current_user()
    print(state.scraper.current_user)
