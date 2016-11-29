import requests
import json
from datetime import datetime


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

    def get(self):
        '''
            GET methods for all the apis
        '''
        return requests.get(self.url,
                            params=self.payload,
                            headers=self.headers)

    def post(self):
        '''
            POST methods for all the apis
        '''
        return requests.post(self.url,
                             params=self.payload,
                             headers=self.headers)


class ApiManagement(ApiSimplyMeasured):
    '''
        Apis for simply measured account management
    '''

    # Base url
    BASE_URL = 'v1/management/'

    def __init__(self, token):
        ApiSimplyMeasured.__init__(self)
        self.url = self.url + ApiManagement.BASE_URL
        self.headers['Authorization'] = "Bearer " + token

    def parseJson(self, data):
        '''
        Convert byte to json and return data key if exists
        '''
        data = data.decode("utf-8")
        data = json.loads(data)
        return data.get('data', {})

    def get_sm_accounts(self, data_source_types='instagram_user'):
        '''
        Get simply measured accounts
        '''
        self.url = self.url + 'accounts'
        self.payload['data_source_types'] = data_source_types
        result = self.parseJson(self.get().content)
        return self.get_sm_account_json(result)

    def get_sm_account_json(self, results):
        '''
        Convert simply measured accounts to json array according to model
        '''
        lst_json = []
        for result in results:
            temp_json = {}
            temp_json['sm_id'] = result.get('id', None)
            attributes = result.get('attributes', None)
            if attributes:
                temp_json['name'] = attributes.get('name', '')
                temp_json['is_active'] = attributes.get('is_active', True)
                temp_json['created_at'] = self.parse_date(
                    attributes.get('created_at'))
                temp_json['updated_at'] = self.parse_date(
                    attributes.get('updated_at'))
                temp_json['created_by'] = attributes.get('created_by')
                temp_json['updated_by'] = attributes.get('updated_by')
                temp_json['image_url'] = attributes.get('image_url')
                temp_json['account_utilization'] = attributes.get(
                    'account_utilization')
            lst_json.append(temp_json)

        return lst_json

    def get_sm_data_sources(self, data_source_types='instagram_user'):
        # TODO:Working on saving
        self.url = self.url + 'data-sources'
        self.payload['data_source_types'] = data_source_type
        result = self.parseJson(self.get().content)
        return result
