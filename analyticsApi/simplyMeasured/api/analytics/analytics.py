import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.ApiSimplyMeasured.api.simplyMeasured import ApiSimplyMeasured
from analyticsApi.ApiSimplyMeasured.api.simplyMeasured.api.analytics.jsonParse import JsonAnalytics


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

    # def get_all_posts(self, channel_type='instagram'):
    #     lst_result = []
    #     for account in SmAccount.objects.all():
    #         lst_result = lst_result + \
    #             self.get_post_by_account(account, channel_type)
    #     return lst_result

    # def get_post_by_account(self, account, channel_type, limit=1000):
    #     self.payload['sort'] = 'post.creation_date:asc'
    #     sm_account_id = account.sm_id
    #     self.url = self.url + str(sm_account_id) + '/posts'
    #     self.payload['filter'] = 'channel.eq(' + channel_type + ')'
    #     self.payload['limit'] = limit
    #     for profile in Profile.objects.filter(sm_account=account):
    #         self.get_post_by_profile(profile, limit)

    def get_posts_by_profile(self, profile,
                             sm_account_id=None, query_params=None):
        if sm_account_id:
            self.url = self.url + str(sm_account_id) + '/posts'
        else:
            self.url = self.url + str(profile.sm_account.sm_id) + '/posts'

        if query_params:
            self.payload = {**self.payload, **query_params}
        result = self.get_all(JsonAnalytics.get_posts_by_profile_callback)

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
        self.payload['limit'] = 1000
        # TODO add paging
        if profile_id:
            # TODO self.payload['filter'] = 'channel.eq(' + channel_type + ')'
            pass
        result = self.parseJson(self.get().content)
        return JsonAnalytics.get_profiles_json(result, account.id)
