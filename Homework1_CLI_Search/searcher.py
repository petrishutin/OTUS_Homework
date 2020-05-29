import argparse

recursion = False
recur_depth = 1


def yandex_start(request: str):
    return request


def google_start(request: str):
    return request


def recursive_search(start_point: 'html', reqursion_depth: int, log_file: str, blind: bool):
    print(start_point, recur_depth, log_file, blind)


def main():
    """This function in for CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help="Input your request. Use '_' for spaces between words;")
    parser.add_argument('-e', '--engine', type=str, default='yandex',
                        help="Choose search engine. Yandex and Google are available;")
    parser.add_argument('-r', '--recursion', type=int, default=0,
                        help="Input depth or recursion of search. Max value is 10;")
    parser.add_argument('-f', '--file', type=str,
                        help='Input path/file for output of results. *.json and *.csv formats are supported;')
    parser.add_argument('-b', '--blind', type=bool, default=False, help="Type 'y' to blind results in console;")
    args = parser.parse_args()
    start_key_words = ' '.join(args.request.split('_'))
    yandex_valid_links = ['http:www.//yandex.ru', 'https://www.yandex.ru',
                          'http://yandex.ru', 'https://yandex.ru', 'www.yandex.ru', 'yandex.ru', 'yandex']
    google_valid_links = ['https://www.google.com', 'http://www.google.com',
                          'https://google.com', 'http://google.com', 'www.google.com', 'google.com', 'google']
    if args.engine.lower() in yandex_valid_links:
        start_point = yandex_start(start_key_words)
    elif args.engine.lower() in google_valid_links:
        start_point = google_start(start_key_words)
    else:
        quit('Invalid search engine. Choose yandex or google')
    recursion_depth = args.recursion
    if recursion_depth > 10:
        quit(f'{recursion_depth} times recursions is too deep. Define 10 times recursion 10 or less')
    file = args.file
    blind = bool(args.blind)

    recursive_search(start_point, recursion_depth, file, blind)

if __name__ == '__main__':
    main()
