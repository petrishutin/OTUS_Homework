import json

import argparse
import requests
from bs4 import BeautifulSoup

TOKEN = 'AIzaSyAz2wfHn9E6OpFq8Bdlt75EDGJ7dHSxymM' #'AIzaSyCerh5TjiWijNJtT3zf_OuCj7ZTIYRJ4ng'
# sing in into google account and get token at https://developers.google.com/custom-search/v1/introduction
DEBUG = True


def google_api_search(search_phrase: str, number_of_results: int, token: str) -> dict:
    """Func to build initial pool of results """
    # TODO add catching Invalid and Expired key errors
    search_phrase = search_phrase.replace('_', '+')
    number_req = f'&num={number_of_results}'
    url = f'https://www.googleapis.com/customsearch/v1?key={token}&cx=017576662512468239146:omuauf_lfve{number_req}&q={search_phrase}'
    response = requests.get(url)
    try:
        resp_body = response.json()
    except AttributeError as e:
        if DEBUG:
            print(e)  # TODO add error logging
    if DEBUG:
        print(resp_body)
    found_results = dict()
    try:
        resp_body['items']
    except KeyError:
        quit('No results found')
    for item in resp_body['items']:
        name = item['htmlTitle'].replace('<b>', '').replace('</b>', '')
        found_results[name] = item['link']
    return found_results


class Searcher:
    def __init__(self, url: str, recursion_depth: int, log_file: str):
        self.url = url
        self.recursion_depth = recursion_depth
        self.logger = Logger(log_file)
        self.found_results = {}
        self.response = None
        self._requesting()
        self._parsing()
        self._building_pool()

    def _requesting(self):
        try:
            self.response = requests.get(self.url)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema,
                requests.exceptions.SSLError,
                ConnectionError,) as e:
            if DEBUG:
                print(e)  # TODO add error log

    def _parsing(self):
        if not self.response or not 199 < self.response.status_code < 300:
            pass
        else:
            html_body = self.response.text
            parser = BeautifulSoup(html_body, "html.parser")
            links = parser.findAll('a')
            for link in links:
                self.found_results[link.text] = link.get('href')
            if self.found_results:
                self.logger.add(self.found_results)

    def _building_pool(self):
        if self.recursion_depth == 1:
            pass
        else:
            for item in self.found_results:
                # print("item: ", item, 'value:', self.found_results[item])
                Searcher(self.found_results[item],
                         self.recursion_depth - 1, self.log_file)


class Logger:
    __data = dict()
    __log_file = None
    __log_format = None

    def __init__(self, log_file: str = None):
        if log_file is None:
            Logger.__log_format = None
            Logger.__log_file = None
        else:
            ext = None  # To calm down PyCharm
            try:
                _, ext = log_file.split('.')
            except (ValueError, AttributeError):
                quit('Invalid file name')
            if ext in ('json', 'csv'):
                Logger.__log_format = ext
            else:
                quit('Invalid file extension')
            Logger.__log_file = log_file

    @classmethod
    def add(cls, data: dict):
        assert isinstance(data, dict), "Logging data must be a dict"
        cls.__data.update(data)

    @classmethod
    def log(cls):
        to_log = None
        if cls.__log_format == 'json':
            to_log = json.dumps(cls.__data)
        elif cls.__log_format == 'csv':
            to_log = ''
            for item in cls.__data:
                to_log += f"{item}, {cls.__data[item]}\n"
        if cls.__log_format:
            with open(cls.__log_file, 'w') as file:
                file.write(to_log)
        else:
            print('Results found:\n')
            for item in cls.__data:
                print(item, ':', cls.__data[item])


def main():
    """Getting command line args, building CLI and initializing search"""
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help="Input your request. Use '_' for spaces between words;")
    parser.add_argument('-r', '--recursion', type=int, default=1,
                        help="Depth of recursion of search in initial results, if enabled. Max value is 5;")
    parser.add_argument('-n', '--number', type=int, default=20,
                        help="Number of search results for initial search, 20 by default;")
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Input path/file for output of results. *.json and *.csv formats are supported; '
                             'Logging to console by default')
    args = parser.parse_args()
    start_key_words = ' '.join(args.request.split('_'))
    recursion_depth = args.recursion
    if recursion_depth > 5:
        quit(f'{recursion_depth} times recursions is too deep. Define 5 times recursion or less')
    if recursion_depth < 1:
        quit('Recursion should be positive integer above zero.')
    number = args.number
    file = args.file

    args = (start_key_words, number, recursion_depth, file,)

    initial_search = google_api_search(start_key_words, number, TOKEN)
    Logger(file)
    Logger.add(data=initial_search)
    if recursion_depth == 1:
        Logger.log()
        quit('Done')
    for res in initial_search:
        Searcher(initial_search[res], recursion_depth, None)


if __name__ == '__main__':
    main()
