"""Script to fetch all language compilers in JSON
It is used only to 'build' distribution, do not use it
"""

from bs4 import BeautifulSoup
import sys
sys.path.append('..')
from codeforces_scraper import Scraper
from getpass import getpass
from pydantic import BaseModel
from typing import List

class LanguageCompiler(BaseModel):
    id: int
    name: str
    extensions: List[str]


class LanguageList(BaseModel):
    __root__: List[LanguageCompiler]


scraper = Scraper()
scraper.login(input(), getpass())
soup = BeautifulSoup(scraper.get('problemset/problem/4/A').text, 'lxml')
subject_options = [i.findAll('option') for i in soup.findAll('select', attrs={'name': 'programTypeId'})][0]
models = LanguageList(__root__=[LanguageCompiler(id=i['value'], name=i.text, extensions=[]) for i in subject_options])
print(models.json())
