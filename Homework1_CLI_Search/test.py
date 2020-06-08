import requests
from pprint import  pprint

api_key='AIzaSyCerh5TjiWijNJtT3zf_OuCj7ZTIYRJ4ng'
search_phrase = 'otus'.replace(' ', '+')
number_of_results = 3
number_req = f'&num={number_of_results}'
url = f'https://www.googleapis.com/customsearch/v1?key={api_key}' \
      f'&cx=017576662512468239146:omuauf_lfve{number_req}&q={search_phrase}'
response = requests.get(url)
js = response.json()
print(js)
pprint(js['items'])
found_results = dict()
for item in js['items']:
    name = item['htmlTitle'].replace('<b>', '').replace('</b>', '')
    found_results[name] = item['link']
print(found_results)

