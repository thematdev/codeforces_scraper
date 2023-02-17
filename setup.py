import setuptools

setuptools.setup(
        name='codeforces-scraper',
        version='0.3.0',
        author='thematdev',
        author_email='thematdev@thematdev.org',
        description='Utility to do actions on codeforces',
        packages=['codeforces_scraper', 'codeforces_scraper.assets'],
        install_requires=[
            'bs4',
            'lxml',
            'pydantic',
            'requests',
        ],
        python_requires='>=3.8',
        zip_safe=True,
        package_data={
            'codeforces_scraper.assets': ['*']
        }
)
