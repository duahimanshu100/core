import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.ApiSimplyMeasured.api.simplyMeasured import ApiSimplyMeasured


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
        result = self.get_all(self.get_posts_by_profile_callback)

    def get_posts_by_profile_callback(self, data):
        data = self.parseJson(data.content)
        post_json = self.get_post_json(data)
        print(Utility.save_and_update_data(
            PostSerializer, post_json, Post, 'post_id', 'post_id'))

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
        return self.get_profiles_json(result, account.id)

    def get_post_json(self, results):
        '''
        Convert simply measured data sources to json array according to model
        '''
        lst_json = []
        for result in results:
            try:
                result['attributes']['fields']['channel'] = result[
                    'attributes']['fields'].pop('channel')
                result['attributes']['fields']['post_id'] = result[
                    'attributes']['fields'].pop('post.id')
                result['attributes']['fields']['profile_id'] = result[
                    'attributes']['fields'].pop('author.id')
                result['attributes']['fields']['body'] = result[
                    'attributes']['fields'].pop('post.body')
                result['attributes']['fields']['content_type'] = result[
                    'attributes']['fields'].pop('post.primary_content_type')
                result['attributes']['fields']['created_at'] = result[
                    'attributes']['fields'].pop('post.creation_date')
                metrics = result['attributes']['metrics']
                result['attributes']['fields']['engagement_total'] = metrics[
                    'post.engagement_total'] if metrics['post.engagement_total'] else 0
                result['attributes']['fields']['likes_count'] = metrics[
                    'post.likes_count'] if metrics['post.likes_count'] else 0
                result['attributes']['fields'][
                    'replies_count'] = metrics['post.replies_count'] if metrics['post.replies_count'] else 0
                result['attributes']['fields'][
                    'shares_count'] = metrics['post.shares_count'] if metrics['post.shares_count'] else 0

                lst_json.append(result['attributes']['fields'])
            except KeyError:
                pass

        return lst_json

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
                result['attributes']['fields']['audience_count'] = result[
                    'attributes']['metrics'].pop('profile.audience_count')
                result['attributes']['fields']['sm_account'] = account_id
                lst_json.append(result['attributes']['fields'])
            except KeyError:
                pass

        return lst_json
