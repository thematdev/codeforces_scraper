import requests
import re
from requests import Response
from bs4 import BeautifulSoup as bs
from typing import List

MESSAGE_GREP_STRING = r'Codeforces\.showMessage\('
# TODO: Grep for Codeforces.showMessage(" to find message, that has been sent


def unfuck_multitest_sample(sample_input: str) -> str:
    div_class_regex = '<div class="[a-zA-Z0-9- ]*">'
    sample_input = re.sub(div_class_regex, '', sample_input)
    sample_input = re.sub('</div>', '\n', sample_input)
    sample_input = re.sub('<pre>', '', sample_input)
    sample_input = re.sub('</pre>', '', sample_input)
    return sample_input


def create_jar(str_cookie: str):
    cookies = str_cookie.split(';')
    d = {}
    for c in cookies:
        i = c.find('=')
        k = c[:i]
        v = c[i+1:]
        d[k] = v
    cj = requests.cookies.merge_cookies(requests.cookies.RequestsCookieJar(), d)
    return cj


def get_token(response: Response) -> str:
    text = response.text
    soup = bs(text, 'lxml')
    token = soup.find(class_='csrf-token')['data-csrf']
    return token


# FIXME: More robust way to find messages
def get_messages(response: Response) -> List[str]:
    text = response.text
    return re.findall(fr'{MESSAGE_GREP_STRING}\"(.+?)\"', text)
