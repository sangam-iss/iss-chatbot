import requests
from datetime import datetime
class TouristDatabase():
    def __init__(self,url,key):
        self.url = url
        self.api_key = key

    def get_search_data(self,type='event',keyword = None):
        api = '/content/v1/search/all'
        params = {
            'dataset': type,
            'apikey': self.api_key
        }
        if keyword is not None:
            params['keyword'] = keyword
        req = requests.get(self.url+api, params=params)
        if (req.status_code != 200):
            print(req.status_code)
            print(req.text)
            return None
        response = req.json()
        print(response['data'])
        return response['data']['results']

    def get_tour_data(self,type='tour',category=None):
        api = '/content/v1/search/all'
        params = {
            'dataset': type,
            'apikey': self.api_key,
        }
        if category is not None:
            params['keyword'] = category

        req = requests.get(self.url+api, params=params)
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)
            return None
        response = req.json()
        print("\n\n")
        print(response['data']['results'][0])
        print("\n\n")
        return response['data']['results']