import json
import requests
from codeforces_scraper import Scraper


# TODO: it should be scraper method
def store_session(scraper: Scraper, session_file):
    with open(session_file, 'w') as f:
        d = requests.utils.dict_from_cookiejar(scraper.session.cookies)
        d['__termforces_name'] = scraper.current_user
        json.dump(d, f)


# TODO: it should be a scraper method
def load_session(scraper: Scraper, session_file):
    with open(session_file, 'r') as f:
        d = json.load(f)
        name = d['__termforces_name']
        del d['__termforces_name']
        new_cookies = requests.utils.cookiejar_from_dict(d)
        scraper.current_user = name
        scraper.session.cookies.clear()
        scraper.session.cookies.update(new_cookies)
