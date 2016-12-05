import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer


class ApiSimplyMeasured(object):
    '''
    Base class for calling the simple measured api
    '''

    # Base url of simply shared
    BASE_URL = "https://api.simplymeasured.com/"

    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.payload = {}
        self.url = ApiSimplyMeasured.BASE_URL

    def parse_date(self, str_date, format='%Y-%m-%dT%H:%M:%S.%f%z'):
        '''
            Convert string date of simply measured to date time object
        '''
        return datetime.strptime(str_date, format)

    def parseJson(self, data):
        '''
        Convert byte to json and return data key if exists
        '''
        data = data.decode("utf-8")
        data = json.loads(data)
        return data.get('data', {})

    def get(self):
        '''
            GET methods for all the apis
        '''
        return requests.get(self.url,
                            params=self.payload,
                            headers=self.headers)

    def get_all(self, callback=None):
        '''
            GET methods for all pagging api the apis
            deafult limit is of 1000
            deafult max pagfing is 5
        '''
        result = self.get()
        lst_result = []
        if not callback:
            lst_result.append(result)
        else:
            callback(result)
        count_hit = 1
        if result and result.content and \
                Utility.get_remaining_page_count(result.content):
            remaining = Utility.get_remaining_page_count(result.content)
            while(remaining):
                count_hit = count_hit + 1
                self.payload['page'] = count_hit
                result = self.get()

                if not callback:
                    lst_result.append(result)
                else:
                    callback(result)

                remaining = Utility.get_remaining_page_count(
                    result.content)
        if callback:
            return count_hit
        return lst_result

    def post(self):
        '''
            POST methods for all the apis
        '''
        return requests.post(self.url,
                             params=self.payload,
                             headers=self.headers)
