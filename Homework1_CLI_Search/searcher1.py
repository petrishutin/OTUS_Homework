import json

import argparse
import requests
from bs4 import BeautifulSoup


class Logger:
    __data = dict()
    __log_file = None
    __log_format = None

    def __init__(self, log_file: str = None, ext: str = None):
        if not self.__log_file:
            Logger.__log_file = log_file
        if not self.__log_format:
            Logger.__log_format = ext

    def add(self, data: dict):
        self.__data.update(data)

    @classmethod
    def log(cls):
        to_log = None
        if cls.__log_format == 'json':
            to_log = json.dumps(cls.__data)
        elif cls.__log_format == 'csv':
            to_log = ''
            for item in cls.__data:
                to_log += f"{item}, {cls.__data[item]}\n"
        if cls.__log_file and cls.__log_format:
            with open(cls.__log_file, 'w') as file:
                file.write(to_log)
        else:
            print('Results found:\n')
            for item in cls.__data:
                print(item, ':', cls.__data[item])


class Searcher:
    def __init__(self, url: str, filter_tag: str, number_of_results: int, recursion_depth: int, log_file: str):
        self.url = url
        self.filter_tag = filter_tag
        self.number_of_results = number_of_results
        self.recursion_depth = recursion_depth
        self.log_file = log_file
        self.logger = Logger(*Searcher.__split_name_and_extension(log_file))
        self.found_results = {}
        self.response = None
        self._requesting()
        self._parsing()
        self._building_pool()

    @staticmethod
    def __split_name_and_extension(file_name):
        try:
            _, ext = file_name.split('.')
        except (ValueError, AttributeError):
            return None, None,
        if ext in ('json', 'csv'):
            return file_name, ext
        return None, None

    def _requesting(self):
        """This function """
        if self.url.find('https://duckduckgo.com/') != -1:
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.5',
                       'Connection': 'keep-alive',
                       'Host': 'duckduckgo.com',
                       'Referer': 'https://duckduckgo.com/',
                       'TE': 'Trailers', 'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        else:
            headers = None
        try:
            self.response = requests.get(self.url, headers=headers)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema,
                requests.exceptions.SSLError,
                ConnectionError,) as e:
            print(e)
        print(self.response.text)


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
                print("item: ", item, 'value:', self.found_results[item])
                Searcher(self.found_results[item], '', self.number_of_results,
                         self.recursion_depth - 1, self.log_file)


def main():
    """Building CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help="Input your request. Use '_' for spaces between words;")
    parser.add_argument('-e', '--engine', type=str, default='duckduckgo.com',
                        help="Choose search engine. DuckDuckGo.com are available. DuckDuckGo.com by default;")
    parser.add_argument('-r', '--recursion', type=int, default=1,
                        help="Input depth or recursion of search. Max value is 5. 1 by default;")
    parser.add_argument('-n', '--number', type=int, default=1,
                        help="Number of search results on page or in each recursion level, if recursion is enabled;")
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Input path/file for output of results. *.json and *.csv formats are supported; '
                             'Logging to console by default')
    args = parser.parse_args()
    start_key_words = ' '.join(args.request.split('_'))
    if args.engine.lower() == 'duckduckgo.com':
        first_url = f"https://duckduckgo.com/?q={start_key_words.replace(' ', '+')}"
    else:
        quit('Invalid search engine. Type -e duckduckgo.com')
    recursion_depth = args.recursion
    filter_tag = 'result_a'
    if recursion_depth > 5:
        quit(f'{recursion_depth} times recursions is too deep. Define 5 times recursion or less')
    number = args.number
    file = args.file

    args = (first_url, filter_tag, number, recursion_depth, file,)
    Searcher(*args)
    Logger.log()


if __name__ == '__main__':
    main()
