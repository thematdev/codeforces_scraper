from codeforces_scraper import Scraper, ScraperError
from getpass import getpass
import unittest
from random import randint

CPP_LANG = 54

CONTEST_ID = 4
PROBLEM_INDEX = 'A'

SOURCE = \
    """#include <iostream>

using namespace std;

int main() {
    int w; cin >> w;
    if (w % 2 == 0 && w >= 4) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
}
"""


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.username = input('username: ')
        cls.password = getpass(f'codeforces password for {cls.username}: ')

    def setUp(self):
        self.scraper = Scraper()

    def tearDown(self):
        self.scraper.close()

    def test_simple_login_logout(self):
        self.assertEqual(self.scraper.fetch_current_user(), None)
        self.scraper.login(self.username, self.password)
        self.assertEqual(self.scraper.fetch_current_user(), self.username)
        self.scraper.logout()
        self.assertEqual(self.scraper.fetch_current_user(), None)

    def test_same_submission(self):
        self.scraper.login(self.username, self.password)
        self.assertRaises(ScraperError, self.scraper.submit, CONTEST_ID, PROBLEM_INDEX, SOURCE, CPP_LANG)

    def test_unique_submission(self):
        salt = f'// Salt: {hex(randint(1, 1337666228))}\n'
        source = salt + SOURCE
        self.scraper.login(self.username, self.password)
        self.scraper.submit(CONTEST_ID, PROBLEM_INDEX, source, CPP_LANG)

    def test_submit_while_not_logged_in(self):
        self.assertRaises(ScraperError, self.scraper.submit, CONTEST_ID, PROBLEM_INDEX, SOURCE, CPP_LANG)

    def test_get_submissions(self):
        self.scraper.get_submissions(CONTEST_ID, self.username)
