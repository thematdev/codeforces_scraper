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

## Termforces
Termforces is a CLI wrapper for scraper. Currently it has a python module and a shell script

## Quickstart
Use `termforces login <username>` to login, it will store your session,
so you're not needed to do it often.

Then enter a directory you want and use `termforces strap --contest-id <contest_id> --indices <indices>`.

Indices should be separated with space, i.e `termforces strap --contest-id 1329 --indices "A B1 B2 C D E"`.
It will create folders `problem$index` for each index you specified.

You may also specify template folder with `--template <path-to-template-folder>`, in this case script will copy
its contents to all problem subfolders.

You can check your results with `termforces results` and submit files with `termforces submit <filename>`.
Script will determine contest id from parent .rc file and problem index from folder name. You may run it either from parent or from child
directory.
