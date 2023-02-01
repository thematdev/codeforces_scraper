import click
from termforces.termforces_shell import termforces_shell, State
from codeforces_scraper import Verdict
from codeforces_scraper.languages import some_compiler_by_ext
from termforces.utils import tcolors, str_from_timestamp


@termforces_shell.command(name='enter-contest')
@click.argument('contest_id')
@click.pass_obj
def enter_contest(state: State, contest_id: int):
    state.contest_id = contest_id


@termforces_shell.command(name='submit')
@click.argument('problem_index')
@click.argument('source_file')
@click.option('--contest-id')
@click.option('--lang-code')
@click.pass_obj
def submit(state: State, problem_index, source_file, contest_id, lang_code):
    if contest_id is None:
        if state.contest_id is not None:
            contest_id = state.contest_id
        else:
            print('Specify contest id or enter contest via enter-contest command')
            return
    if lang_code is None:
        ext = '.' + source_file.split('.')[-1]
        compiler = some_compiler_by_ext(ext)
        if compiler is None:
            print('Please specify language code')
            return
        lang_code = compiler.id
    with open(source_file, 'r') as f:
        source_code = f.read()
    state.scraper.submit(contest_id, problem_index, source_code, lang_code)


@termforces_shell.command(name='results-my')
@click.option('--contest-id')
@click.pass_obj
def results_my(state: State, contest_id):
    if contest_id is None:
        if state.contest_id is not None:
            contest_id = state.contest_id
        else:
            print('Specify contest id or enter contest via enter-contest command')
            return
    if state.scraper.current_user is None:
        print('Please login to view your results')
        return
    subms = state.scraper.get_submissions(contest_id, state.scraper.current_user)
    subms.sort(key=lambda subm: (subm.problem.index, subm.creation_time_seconds))

    for subm in subms:
        if subm.verdict == Verdict.TESTING:
            color = tcolors.WARNING
        elif subm.verdict == Verdict.OK:
            color = tcolors.OKGREEN
        else:
            color = tcolors.FAIL
        verdict_str = f'{color}{subm.verdict.name}{tcolors.ENDC}'
        print(f'{subm.problem.index} \t {str_from_timestamp(subm.creation_time_seconds)} \t {verdict_str}')
