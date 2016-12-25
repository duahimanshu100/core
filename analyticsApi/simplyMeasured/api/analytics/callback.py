from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.analytics.jsonParse import JsonAnalytics
from analyticsApi.serializers import PostSerializer,PostShareSerializer,PostSerializerCreate,PostHashTagSerializer,PostLikeSerializer, PostCommentSerializer, PostFilterSerializer,PostMetricSerializer
from analyticsApi.models import Post, PostHashTag,PostFilter, PostMetric
from datetime import datetime

class AnalyticsCallback:

    @staticmethod
    def get_posts_by_profile_callback(data):
        '''
        Get and save all post according to profile
        '''
        print('Start Saving Posts & Related Data at ' + str(datetime.now()))
        post_json , hash_json, metrics_json, filters_json = JsonAnalytics.get_post_json(data)
        # import pdb
        # pdb.set_trace()
        dict_post = dict(Post.objects.filter(profile_id=post_json[0]['profile_id']).values_list('post_id', 'id'))

        def filter_only_create_post(obj_json):
            if(obj_json.get('post_id')):
                return  obj_json['post_id'] not in dict_post
            else:
                return obj_json['post_id_id'] not in dict_post

        posts = filter(filter_only_create_post, PostSerializerCreate(post_json, many=True).data)
        hashes = filter(filter_only_create_post, hash_json)
        # likes = filter(filter_only_create_post, likes_json)
        # shares = filter(filter_only_create_post, shares_json)
        # replies = filter(filter_only_create_post, replies_json)
        filters = filter(filter_only_create_post, filters_json)
        import pdb
        pdb.set_trace()

        Post.objects.bulk_create([Post(**i) for i in posts])
        PostHashTag.objects.bulk_create([PostHashTag(**i) for i in hashes])
        PostFilter.objects.bulk_create([PostFilter(**i) for i in filters])


        post_ids = [i['post_id'] for i in post_json]

        PostMetric.objects.filter(post_id__in= post_ids,is_latest=True).update(is_latest=False)
        # PostShare.objects.filter(post_id__in=post_ids, is_latest=True).update(is_latest=False)
        # PostComment.objects.filter(post_id__in=post_ids, is_latest=True).update(is_latest=False)


        PostMetric.objects.bulk_create([PostMetric(**i) for i in metrics_json])
        # PostShare.objects.bulk_create([PostShare(**i) for i in shares_json])
        # PostComment.objects.bulk_create([PostComment(**i) for i in replies_json])
        print('Finished  Saving Posts & Related Data at ' + str(datetime.now()))
        # print(post_json)
        # import pdb
        # pdb.set_trace()
        # print(Utility.save_and_update_data(
        #     PostSerializer, post_json, Post, 'post_id', 'post_id'))
