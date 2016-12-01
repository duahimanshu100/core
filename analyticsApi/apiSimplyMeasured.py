import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount
from analyticsApi.utility import Utility


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
        '''
        Get simply measured data sources for data sources
        '''
        # Fix the Comma Seperated String
        resultSet = SmAccount.objects.all().values_list('sm_id', flat=True)
        finalResult = Utility.list_to_comma_seperated_string(resultSet)
        self.url = self.url + 'data-sources'
        self.payload['data_source_types'] = data_source_types
        self.payload['account_ids'] = finalResult
        result = self.parseJson(self.get().content)
        return self.get_sm_data_source_json(result)

    def get_sm_data_source_json(self, results):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            temp_json = {}
            temp_json['ds_id'] = result.get('id', None)
            attributes = result.get('attributes', None)
            relationships = result.get('relationships', None)
            relationships = relationships.get('account', None)
            relationships = relationships.get('data', None)
            accountId = relationships.get('id', None)
            if attributes:
                sm_account = SmAccount.objects.get(
                    sm_id=accountId)
                temp_json['sm_account'] = sm_account.id
                temp_json['provided_name'] = attributes.get(
                    'provided_name', None)
                temp_json['status'] = attributes.get('status', '')
                temp_json['created_at'] = self.parse_date(
                    attributes.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
                temp_json['updated_at'] = self.parse_date(
                    attributes.get('updated_at'), '%Y-%m-%dT%H:%M:%SZ')
                temp_json['provided_description'] = attributes.get(
                    'provided_description', None)
                temp_json['data_source_type'] = attributes.get(
                    'data_source_type')
                temp_json['value'] = attributes.get('value')
                temp_json['sentiment_enabled'] = attributes.get(
                    'sentiment_enabled')
                temp_json['elevated_access'] = attributes.get(
                    'elevated_access')
                temp_json['canonical_id'] = attributes.get(
                    'canonical_id')
                # add feature
                temp_json['feature'] = attributes.get('features', None)

            lst_json.append(temp_json)

        return lst_json


class ApiAnalytics(ApiSimplyMeasured):
    '''
        Apis for simply measured account management
    '''

    # Base url
    BASE_URL = 'v1/analytics/'

    def __init__(self, token):
        ApiSimplyMeasured.__init__(self)
        self.url = self.url + ApiAnalytics.BASE_URL
        self.headers['Authorization'] = "Bearer " + token

    def get_profiles(self, channel_type='instagram'):
        '''
        Get social profiles by simply measured
        '''
        lst_result = []
        for account in SmAccount.objects.all():
            lst_result = lst_result + \
                self.get_profile_by_account(account, channel_type)
        return lst_result

    def get_profile_by_account(self, account,
                               channel_type='instagram',
                               profile_id=''):
        sm_account_id = account.sm_id
        self.url = self.url + sm_account_id + '/profiles'
        self.payload['filter'] = 'channel.eq(' + channel_type + ')'
        self.payload['limit'] = 10000
        # TODO add paging
        if profile_id:
            # TODO self.payload['filter'] = 'channel.eq(' + channel_type + ')'
            pass
        result = self.parseJson(self.get().content)
        return self.get_profiles_json(result, account.id)

    def get_profiles_json(self, results, account_id):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            try:
                result['attributes']['fields']['profile_id'] = int(result[
                    'attributes']['fields'].pop('profile.id'))
                result['attributes']['fields']['channel_type'] = result[
                    'attributes']['fields'].pop('channel')
                result['attributes']['fields']['link'] = result[
                    'attributes']['fields'].pop('profile.link')
                result['attributes']['fields']['handle'] = result[
                    'attributes']['fields'].pop('profile.handle')
                result['attributes']['fields']['display_name'] = result[
                    'attributes']['fields'].pop('profile.display_name')
                result['attributes']['fields']['sm_account'] = account_id
                lst_json.append(result['attributes']['fields'])
            except KeyError:
                pass

        return lst_json
