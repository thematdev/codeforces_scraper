import setuptools

setuptools.setup(
        name='codeforces-scraper',
        version='0.2.0-r1',
        author='thematdev',
        author_email='thematdev@thematdev.org',
        description='Utility to do actions on codeforces',
        packages=['codeforces_scraper', 'codeforces_scraper.assets',
                  'termforces', 'termforces.cmds'],
        scripts=['scripts/termforces'],
        install_requires=[
            'bs4',
            'lxml',
            'pydantic',
            'requests',
            'click',
            'click_shell'
        ],
        python_requires='>=3.8',
        zip_safe=True,
        package_data={
            'codeforces_scraper.assets': ['*']
        }
)
