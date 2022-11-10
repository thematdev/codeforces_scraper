import requests
import re
from requests import Response
from bs4 import BeautifulSoup as bs
from typing import List

MESSAGE_GREP_STRING = r'Codeforces\.showMessage\('
# TODO: Grep for Codeforces.showMessage(" to find message, that has been sent


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


def get_messages(response: Response) -> List[str]:
    text = response.text
    return re.findall(fr'{MESSAGE_GREP_STRING}\"(.+?)\"', text)
