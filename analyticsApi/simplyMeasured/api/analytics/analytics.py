import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.simplyMeasured.api.simplyMeasured import ApiSimplyMeasured
from analyticsApi.simplyMeasured.api.analytics.jsonParse import JsonAnalytics
from analyticsApi.simplyMeasured.api.analytics.callback import AnalyticsCallback


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

    def get_posts(self, sm_account_id, query_params=None):
        self.url = self.url + str(sm_account_id) + '/posts'
        if query_params:
            self.payload.update(**query_params)
            # self.payload = {**self.payload, **query_params}
        result = self.get_all(AnalyticsCallback.get_posts_by_profile_callback)

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
        if profile_id:
            # TODO self.payload['filter'] = 'channel.eq(' + channel_type + ')'
            pass
        result = self.parseJson(self.get().content)
        return JsonAnalytics.get_profiles_json(result, account.id)

    def get_profile_likes(self, sm_account_id, profile_id, query_params=None):
        '''
        Get profile likes
        '''
        self.url = self.url + str(sm_account_id) + '/posts/metrics'
        if query_params:
            self.payload.update(**query_params)
        result = self.parseJson(self.get().content)
        return JsonAnalytics.get_profiles_likes_json(result, profile_id)
