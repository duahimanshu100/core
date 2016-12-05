from analyticsApi.ApiSimplyMeasured.utility import SmUtility
from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.analytics.jsonParse import JsonAnalytics


class AnalyticsCallback:

    @staticmethod
    def get_posts_by_profile_callback(data):
        post_json = JsonAnalytics.get_post_json(data)
        print(Utility.save_and_update_data(
            PostSerializer, post_json, Post, 'post_id', 'post_id'))
