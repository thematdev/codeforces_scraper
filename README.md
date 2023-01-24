## Codeforces Scraper

Codeforces scraper provides a gentle way to interact with Codeforces

```python3
from codeforces_scraper import Scraper
from codeforces_scraper.languages import some_compiler_by_ext
from getpass import getpass

# Submits my code for problem 4A from your account 
scraper = Scraper()
username = input()
password = getpass()
scraper.login(username, password)
scraper.submit(4, 'A', scraper.get_submission_source(4, 190069788), some_compiler_by_ext('.cpp'))
```

## Installation
### From PyPi
`pip3 install codeforces_scraper`

### From sources

```
git clone https://github.com/thematdev/codeforces_scraper.git
python3 setup.py install
```

## Reference
A comment provided for each function.
