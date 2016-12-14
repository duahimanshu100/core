from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.analytics.jsonParse import JsonAnalytics
from analyticsApi.serializers import PostSerializer
from analyticsApi.models import Post


class AnalyticsCallback:

    @staticmethod
    def get_posts_by_profile_callback(data):
        '''
        Get and save all post according to profile
        '''
        post_json = JsonAnalytics.get_post_json(data)
        print(Utility.save_and_update_data(
            PostSerializer, post_json, Post, 'post_id', 'post_id'))
