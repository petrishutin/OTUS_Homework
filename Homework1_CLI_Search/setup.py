import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ishutin_otus_homework1_cli_searcher',
    version='0.1',
    packages=['searcher'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Allow to make web search requests from command line',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/petrishutin/OTUS_Homework/tree/master/Homework1_CLI_Search',
    author='Petr_Ishutin',
    author_email='ishutin.petr@yandex.ru',
    keywords=['web search', 'cli web search'],
    install_requires=[
        'astroid>=2.4.2',
        'beautifulsoup4>=4.9.1',
        'bs4>=0.0.1',
        'certifi>=2020.4.5.1',
        'chardet>=3.0.4',
        'idna>=2.9',
        'isort>=4.3.21',
        'lazy-object-proxy>=1.4.3',
        'requests>=2.23.0',
        'selenium>=3.141.0',
        'six>=1.15.0',
        'soupsieve>=2.0.1',
        'toml>=0.10.1',
        'typed-ast>=1.4.1',
        'urllib3>=1.25.9',
        'wrapt>=1.12.1',
     ],
    entry_points={
        'console_scripts': [
            'searcher = sercher.searcher:main',
        ]
    },
)