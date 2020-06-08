import json
from pprint import pprint

import argparse
import requests
from bs4 import BeautifulSoup

class Log:
    overall_results = dict()

    def __init__(self, log_file):
        self.log_file = log_file
        self.log_format = None

    @classmethod
    def _def_log_extension(cls):
        if cls.log_file is None:
            _, ext = cls.log_file.split('.')
            if ext == 'csv':
                cls.output = 'csv'
            elif ext == 'json':
                cls.output = 'json'
            else:
                exit('Invalid log file extension. Must be csv or json')


class Searcher:
    overall_results = dict()
    log_file = None
    output = 'console'

    def __init__(self, start_href: str, recursion_depth: int, log_file: str = None):
        if log_file:
            Searcher.log_file = log_file
        self.star_href = start_href
        self.recursion_depth = recursion_depth
        self.log_file = log_file
        self.found_results = dict()
        self.poop_of_threads = []
        self._def_log_extension()

    def run(self):
        self._parsing_link()
        if self.output == 'console':  # printing results to console during run time
            if self.found_results:  # checking if result not void
                pprint(self.found_results)
        self._building_children()

    @classmethod
    def log_to_file(cls):
        print('called')
        if cls.output != "console":
            with open(cls.log_file, 'w') as file:
                if cls.output == 'csv':
                    for item in cls.overall_results:
                        yield file.write(f"'{item}', '{Searcher.overall_results[item]}'\n")
                elif cls.output == 'json':
                    log = json.dumps(Searcher.overall_results)
                    file.write(log)


    def _parsing_link(self):
        try:
            response = requests.get(self.star_href)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema,
                requests.exceptions.SSLError,
                ConnectionError):
            response = None
        if not response:
            pass
        else:
            if not response.status_code == 200:
                print(f'{response.status_code} is Bad response for: {self.star_href}')
            html_body = response.text
            parser = BeautifulSoup(html_body, "html.parser")
            links = parser.findAll('a')
            for link in links:
                self.found_results[link.text] = link.get('href')
            if self.found_results:
                Searcher.overall_results.update(self.found_results)

    def _building_children(self):
        if self.recursion_depth == 1:
            pass
        else:
            for name in self.found_results:
                Searcher(self.found_results[name], self.recursion_depth - 1, self.log_file)


def main():
    """Building CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help="Input your request. Use '_' for spaces between words;")
    parser.add_argument('-e', '--engine', type=str, default='yandex',
                        help="Choose search engine. Yandex.ru and Google.com are available. Yandex by default;")
    parser.add_argument('-r', '--recursion', type=int, default=1,
                        help="Input depth or recursion of search. Max value is 5. 1 by default;")
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Input path/file for output of results. *.json and *.csv formats are supported; '
                             'Logging to console by default')
    args = parser.parse_args()
    start_key_words = ' '.join(args.request.split('_'))
    if args.engine.lower() == 'yandex.ru':
        start_point = f"https://yandex.ru/search/?text={start_key_words.replace('_', '+')}"
    elif args.engine.lower() == 'google.com':
        start_point = f"https://www.google.ru/search?q={start_key_words.replace('_', '+')}"
    else:
        quit('Invalid search engine. Type -e yandex.ru or -e google.com')
    recursion_depth = args.recursion
    if recursion_depth > 5:
        quit(f'{recursion_depth} times recursions is too deep. Define 5 times recursion or less')
    file = args.file

    app = Searcher(start_point, recursion_depth, file)
    app.run()
    app.log_to_file()

if __name__ == '__main__':
    main()
