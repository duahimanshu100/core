from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.analytics.jsonParse import JsonAnalytics
from analyticsApi.serializers import PostSerializer, PostShareSerializer, PostSerializerCreate, PostHashTagSerializer, PostLikeSerializer, PostCommentSerializer, PostFilterSerializer, PostMetricSerializer
from analyticsApi.models import Post, PostHashTag, PostFilter, PostMetric, PostLatestMetric
from datetime import datetime


class AnalyticsCallback:

    @staticmethod
    def get_posts_by_profile_callback(data, extra_data=None):
        '''
        Get and save all post according to profile
        '''
        post_json, hash_json, metrics_json, filters_json = JsonAnalytics.get_post_json(
            data, extra_data)
        if(post_json):
            profile_id = post_json[0]['profile_id']
            print('Start Saving Posts & Related Data at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            dict_post = dict(Post.objects.filter(
                profile_id=profile_id).values_list('post_id', 'id'))

            def filter_only_create_post(obj_json):
                if(obj_json.get('post_id')):
                    return obj_json['post_id'] not in dict_post
                else:
                    return obj_json['post_id_id'] not in dict_post

            posts = filter(filter_only_create_post,
                           PostSerializerCreate(post_json, many=True).data)
            hashes = filter(filter_only_create_post, hash_json)
            filters = filter(filter_only_create_post, filters_json)
            print('Post Objects at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            Post.objects.bulk_create([Post(**i) for i in posts])
            print('Post Hashtag Objects at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            PostHashTag.objects.bulk_create([PostHashTag(**i) for i in hashes])
            print('Post Filter Objects at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            PostFilter.objects.bulk_create([PostFilter(**i) for i in filters])

            post_ids = [i['post_id'] for i in post_json]
            print('Post Metric To Deleted at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            PostLatestMetric.objects.filter(
                post_id__in=post_ids).delete()
            print('Post Latest Metric Save Objects at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            PostLatestMetric.objects.bulk_create(
                [PostLatestMetric(**i) for i in metrics_json])
            # print('Post Old Metric To False Objects at ' +
            #       str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
            # # Saving all the metrics
            # PostMetric.objects.bulk_create(
            #     [PostMetric(**i) for i in metrics_json])
            print('Finished  Saving Posts & Related Data at ' +
                  str(datetime.now()) + ' - ProfileId - ' + str(profile_id))
