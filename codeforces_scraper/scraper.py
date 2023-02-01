import requests

from requests import Session
from bs4 import BeautifulSoup as bs

from codeforces_scraper.utils import get_token, get_messages, create_jar
from codeforces_scraper.models import Submission, Problem
from typing import List


BASE_URL = 'https://codeforces.com'


class ScraperError(Exception):
    pass


class MessagedScrapError(ScraperError):
    def __init__(self, codeforces_message: str):
        self.codeforces_message = codeforces_message

    def __str__(self):
        return f'Codeforces returned message, which is not considered as good: {self.codeforces_message}'


class CodeforcesAPIException(ScraperError):
    def __init__(self, comment: str):
        self.comment = comment

    def __str__(self):
        return f'Request to Codeforces API failed. Comment: {self.comment}'


class Scraper:
    def __init__(self, create_session=True, base_url=BASE_URL):
        """Initialize scraper
        If ``create_session`` is True(default), will create session,
        ``base_url`` (default 'codeforces.com') describes URL
        to which all requests will be sent
        """
        self.session = Session() if create_session else None
        self.base_url = base_url
        self.current_user = None

    def close(self):
        """Close scraper(closes session it is not None)"""
        if self.session is not None:
            self.session.close()

    def logout(self):
        """Logout from codeforces
        Does nothing if you're not logged in
        """
        if self.current_user is None:
            return
        soup = bs(self.get().text, 'lxml')
        refs = soup.find(class_='lang-chooser').find_all('a')
        for ref in refs:
            if 'logout' in ref['href']:
                self.get(ref['href'])
                self.update_current_user()
                if self.current_user is not None:
                    raise ScraperError('Failed to logout!')
                return
    
    def get_csrf_token(self):
        """Get csrf token, which is needed
        to make requests by hand
        """
        return get_token(self.get())

    def fetch_current_user(self):
        """Fetch current user by querying codeforces"""
        soup = bs(self.get().text, 'lxml')
        avatar_element = soup.find(class_='avatar')
        if avatar_element is None:
            return None
        return avatar_element.find('div').find('a').text

    def update_current_user(self):
        """Update cached ``current_user`` variable"""
        self.current_user = self.fetch_current_user()

    # Tries to login with given credentials, will relogin, if logged under another user
    def login(self, username: str, password: str):
        """Login to codeforces by ``username`` and ``password``"""
        if self.current_user == username:
            return
        if self.current_user is not None:
            self.logout()
        token = get_token(self.get('enter'))
        payload = {
            'csrf_token': token,
            'action': 'enter',
            'handleOrEmail': username,
            'password': password,
            'remember': 'on'
        }
        self.post('enter', data=payload)
        self.update_current_user()
        if self.current_user != username:
            # TODO: Parse response and raise different errors(if they can be)
            raise ScraperError('Failed to login!')

    def set_cookies_from_header(self, str_cookie: str):
        self.session.cookies = create_jar(str_cookie)

    def submit(self, contest_id: int, problem_index, source_code: str, lang: int) -> None:
        """Submit code in problem ``BASE_URL/contest_id/problem_index`` with source
        ``source_code`` and language code ``lang``.
        Get your language code using Language class
        """
        if self.current_user is None:
            raise ScraperError('Submitting while not logged in')
        url = f'contest/{contest_id}/submit'
        submit_page_response = self.get(url)
        for message in get_messages(submit_page_response):
            raise MessagedScrapError(message)
        token = get_token(submit_page_response)
        payload = {
            'csrf_token': token,
            'source': source_code,
            'submittedProblemIndex': problem_index,
            'action': 'submitSolutionFormSubmitted',
            'programTypeId': lang
        }
        post_response = self.post(url, data=payload)
        if len(get_messages(post_response)) == 0:
            raise ScraperError("Failed to submit. No success message found")

    def make_manual_hack(self, submission_id: int, test_data: str) -> None:
        """Make manual hack(explicit test) of submission with id
        ``submission_id`` and test ``test_data``
        """
        if self.current_user is None:
            raise ScraperError('Hacking while not logged in')
        url = 'data/challenge'
        payload = {
                'csrf_token': self.get_csrf_token(),
                'action': 'challengeFormSubmitted',
                'submissionId': submission_id,
                'inputType': 'manual',
                'testcase': test_data
        }
        self.post(url, data=payload)

    def get_submission_source(self, contest_id: int, submission_id: int) -> str:
        """Get source code of submission by ``contest_id`` and ``submission_id``"""
        url = f'contest/{contest_id}/submission/{submission_id}'
        page_response = self.get(url)
        soup = bs(page_response.text, 'lxml')
        srcs = soup.find_all('pre', attrs={'id': 'program-source-text'})
        try:
            return srcs[0].contents[0]
        except IndexError:
            raise ScraperError("Submission not found!")

    def get_submissions(self, contest_id: int, username: str) -> List[Submission]:
        """Get all submissions in contest ``contest_id``
        of user with handle ``username``, if None returns all submissions
        in this contest
        """
        if username is not None:
            params = {
                'contestId': contest_id,
                'handle': username
            }
        else:
            params = {'contestId': contest_id}
        return [Submission.parse_obj(x) for x in self.api_request('contest.status', params)]

    def get_contest_tasks(self, contest_id: int) -> List[Problem]:
        """Get all tasks in contest with id ``contest_id``"""
        params = {
            'from': 1,
            'count': 1
        }
        return self.api_request('contest.standings', params)['problems']

    def get(self, sub_url='', **kwargs):
        """Make a GET request to BASE_URL"""
        url = self.base_url + '/' + sub_url
        if self.session is not None:
            return self.session.get(url, **kwargs)
        else:
            return requests.get(url, **kwargs)

    def post(self, sub_url='', **kwargs):
        """Make a POST request to BASE_URL"""
        url = self.base_url + '/' + sub_url
        if self.session is not None:
            return self.session.post(url, **kwargs)
        else:
            return requests.post(url, **kwargs)

    def api_request(self, method: str, params):
        """Make a request to Codeforces API with ``params``"""
        resp = self.get(f'api/{method}', params=params)
        try:
            response = resp.json()
        except ValueError:
            # It actually had already happened when Mike
            # decided to turn off API and return HTML instead
            raise ScraperError('API returned invalid JSON')
        if response['status'] == 'FAILED':
            raise CodeforcesAPIException(response['comment'])
        return response['result']
