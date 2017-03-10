import dateutil.parser
from analyticsApi.serializers import PostMetricSerializer, PostsListSerializer, PostWithMetricSerializer, PostHashTagSerializer, PostFilterSerializer, PostWithLatestMetricSerializer, PostLatestMetricSerializer
from django.db.models import Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.utility import Utility
from analyticsApi.models import PostMetric, ProfileEngagementMetric, PostLatestMetric
from django.db import connection
from django.db.models import Max


class FollowersGainedApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model

    def list(self, request, *args, **kwargs):
        sql = '''
            SELECT DISTINCT ON (created_at::date) created_at::date, audience_count
            FROM public."analyticsApi_profilemetric" WHERE profile_id = %s
            ORDER BY created_at::date DESC LIMIT 30;
        '''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EngagementAverageApi(generics.RetrieveAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        pass

    def get(self, request, *args, **kw):
        profile_id = self.kwargs['profile_id']
        queryset = ProfileEngagementMetric.objects.filter(
            profile_id=profile_id, engagement_type=1).first()
        response = Response(queryset.json_response, status=status.HTTP_200_OK)
        return response


class EngagementFrequencyApi(generics.RetrieveAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        pass

    def get(self, request, *args, **kw):
        profile_id = self.kwargs['profile_id']
        queryset = ProfileEngagementMetric.objects.filter(
            profile_id=profile_id, engagement_type=2).first()
        response = Response(queryset.json_response, status=status.HTTP_200_OK)
        return response


class PostMetricListApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostLatestMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(
            profile_id=profile_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        filter = self.request.query_params.get('filter', None)

        if from_date:
            from_date = dateutil.parser.parse(from_date)
            queryset = queryset.filter(post__created_at__gte=from_date)
        if to_date:
            to_date = dateutil.parser.parse(to_date)
            queryset = queryset.filter(post__created_at__lte=to_date)

        if filter:
            queryset = queryset.filter(post__primary_content_type=filter)

        queryset = queryset.aggregate(avg_like=Avg('like_count'),
                                      avg_comment=Avg('comment_count'),
                                      total_like=Sum('like_count'),
                                      total_comment=Sum('comment_count'),
                                      )
        return Response(queryset)


class ProfileLikeHistoryApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):

        sql = '''SELECT metric.created_at::date, CASE WHEN SUM(metric.like_count) - lag(SUM(metric.like_count)) OVER (ORDER BY metric.created_at::date ASC) > 0 THEN SUM(metric.like_count) - lag(SUM(metric.like_count)) OVER (ORDER BY metric.created_at::date ASC) ELSE 0 END as like_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, like_count FROM public."analyticsApi_postmetric" WHERE profile_id = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at DESC'''
        if(self.request.query_params.get('limit', '')):
            sql = sql + ' LIMIT ' + self.request.query_params.get('limit')

        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class ProfileCommentHistoryApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        sql = '''SELECT metric.created_at::date, CASE WHEN SUM(metric.comment_count) - lag(SUM(metric.comment_count)) OVER (ORDER BY metric.created_at::date ASC) > 0 THEN SUM(metric.comment_count) - lag(SUM(metric.comment_count)) OVER (ORDER BY metric.created_at::date ASC) ELSE 0 END as comment_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, comment_count FROM public."analyticsApi_postmetric" WHERE profile_id = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at DESC'''
        if(self.request.query_params.get('limit', '')):
            sql = sql + ' LIMIT ' + self.request.query_params.get('limit')
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class ProfileEngagementHistoryApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        sql = '''SELECT metric.created_at::date, CASE WHEN SUM(metric.engagement_count) - lag(SUM(metric.engagement_count)) OVER (ORDER BY metric.created_at::date ASC) > 0 THEN SUM(metric.engagement_count) - lag(SUM(metric.engagement_count)) OVER (ORDER BY metric.created_at::date ASC) ELSE 0 END as engagement_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, engagement_count FROM public."analyticsApi_postmetric" WHERE profile_id = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at DESC'''
        if(self.request.query_params.get('limit', '')):
            sql = sql + ' LIMIT ' + self.request.query_params.get('limit')
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class RecentPostApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostsListSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(
            profile_id=profile_id).exclude(image_urls__isnull=True)
        return queryset

    def list(self, request, *args, **kwargs):
        limit_by = int(self.request.query_params.get('limit', 5))
        type_of_recent = self.request.query_params.get('order', 'most')
        queryset = self.get_queryset()
        # 2016-12-02T17:00:25.910711
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        filter = self.request.query_params.get('filter', None)

        if from_date:
            from_date = dateutil.parser.parse(from_date)
            queryset = queryset.filter(created_at__gte=from_date)
        if to_date:
            to_date = dateutil.parser.parse(to_date)
            queryset = queryset.filter(created_at__lte=to_date)

        if filter:
            queryset = queryset.filter(primary_content_type=filter)

        order_by_type = '-' if type_of_recent == 'most' else ''
        queryset = queryset.order_by(order_by_type + 'created_at')[:limit_by]
        post_metrics = PostLatestMetric.objects.filter(
            post_id__in=queryset)
        serializer = PostWithLatestMetricSerializer(post_metrics, many=True)
        if order_by_type:
            return Response(reversed(sorted(serializer.data, key=lambda x: x['post_id']['created_at'])))
        else:
            return Response(sorted(serializer.data, key=lambda x: x['post_id']['created_at']))


class OperationPostApi(generics.ListAPIView):
    '''
    Most and least like
    '''
    serializer_class = PostWithLatestMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(
            profile_id=profile_id).exclude(post_id__image_urls__isnull=True)
        return queryset

    def list(self, request, *args, **kwargs):
        dic_of_operations = {
            'like': 'like_count',
            'comment': 'comment_count',
            'share': 'share_count',
            'engagement': 'engagement_count',
            'dislike': 'dislike_count'
        }
        operation = dic_of_operations.get(
            self.request.query_params.get('type', 'like'), 'like')
        limit_by = int(self.request.query_params.get('limit', 5))
        type_of_recent = self.request.query_params.get(
            'order', 'most')
        queryset = self.get_queryset()
        # 2016-12-02T17:00:25.910711
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        filter = self.request.query_params.get('filter', None)

        if from_date:
            from_date = dateutil.parser.parse(from_date)
            queryset = queryset.filter(post_id__created_at__gte=from_date)
        if to_date:
            to_date = dateutil.parser.parse(to_date)
            queryset = queryset.filter(post_id__created_at__lte=to_date)

        if filter:
            queryset = queryset.filter(post_id__primary_content_type=filter)
        order_by_type = '-' if type_of_recent == 'most' else ''
        queryset = queryset.order_by(order_by_type + operation)[:limit_by]
        serializer = PostWithLatestMetricSerializer(queryset, many=True)
        return Response(serializer.data)


class FilterImpactCommentApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def list(self, request, *args, **kwargs):
        filter = self.request.query_params.get('filter', None)
        sql_filter = ''
        if filter:
            if filter == 'video':
                sql_filter = " AND post.primary_content_type = 'photo' "
            else:
                sql_filter = " AND post.primary_content_type = 'video' "
        sql = '''
        SELECT pf.name, SUM(comment_count) FROM public."analyticsApi_postfilter" pf 
        LEFT JOIN public."analyticsApi_postlatestmetric" pm 
        ON (pm.post_id_id=pf.post_id_id) 
        LEFT JOIN public."analyticsApi_post" post ON (post.post_id=pf.post_id_id) 
        WHERE pf.profile_id = %s ''' + sql_filter + ''' GROUP BY pf.name'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class FilterImpactLikeApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def list(self, request, *args, **kwargs):
        filter = self.request.query_params.get('filter', None)
        sql_filter = ''
        if filter:
            if filter == 'video':
                sql_filter = " AND post.primary_content_type = 'photo' "
            else:
                sql_filter = " AND post.primary_content_type = 'video' "

        sql = '''
        SELECT pf.name, SUM(like_count) FROM public."analyticsApi_postfilter" pf
        LEFT JOIN public."analyticsApi_postlatestmetric" pm ON (pm.post_id_id=pf.post_id_id)
        LEFT JOIN public."analyticsApi_post" post ON (post.post_id=pf.post_id_id)
        WHERE pf.profile_id = %s '''  + sql_filter +   ''' GROUP BY pf.name'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class HashtagPerformanceApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def list(self, request, *args, **kwargs):
        dic_of_operations = {
            'like': 'like_count',
            'comment': 'comment_count',
            'engagement': 'engagement_count'
        }
        operation = dic_of_operations.get(
            self.request.query_params.get('type', 'engagement'), 'like_count')

        filter = self.request.query_params.get('filter', None)
        sql_filter = ''
        if filter:
            if filter == 'video':
                sql_filter = " AND post.primary_content_type = 'photo' "
            else:
                sql_filter = " AND post.primary_content_type = 'video' "

        sql = '''SELECT ph.name, SUM(pm.''' + operation + ''') as ''' + operation + \
            ''' FROM public."analyticsApi_posthashtag" ph LEFT JOIN public."analyticsApi_postlatestmetric" pm ON (pm.post_id_id=ph.post_id_id) LEFT JOIN public."analyticsApi_post" post ON (post.post_id=ph.post_id_id) WHERE ph.profile_id = %s ''' + \
            sql_filter + '''GROUP BY ph.name ORDER BY ''' + operation + ''' DESC'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class FilterEngagementPostApi(generics.ListAPIView):
    '''
    FilterEngagementPostApi
    '''
    serializer_class = PostFilterSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        sql = '''
        SELECT pf.name, cast(sum(pm.engagement_count) as integer) as s_e_c 
        FROM public."analyticsApi_postfilter" pf 
        LEFT JOIN public."analyticsApi_postlatestmetric" pm ON (pm.post_id_id=pf.post_id_id)
        WHERE pf.profile_id = %s GROUP BY pf.name
        ORDER BY s_e_C DESC
        '''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = cursor.fetchall()
            return Response(result)
        finally:
            cursor.close()


class Hour24EngagementApi(generics.ListAPIView):
    '''
    Hour24EngagementApi impact on like
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = self.model.objects.filter(
            post_id_id=post_id)
        return queryset

    def list(self, request, *args, **kwargs):
        dic_of_operations = {
            'like': 'like_count',
            'comment': 'comment_count',
            'share': 'share_count',
            'engagement': 'engagement_count',
            'dislike': 'dislike_count'
        }
        operation = dic_of_operations.get(
            self.request.query_params.get('type', 'like'), 'like_count')
        limit_by = int(self.request.query_params.get('limit', 24))
        queryset = self.get_queryset()

        queryset = queryset.order_by('created_at')[:limit_by]
        serializer = PostMetricSerializer(queryset, many=True)
        serialized_data = serializer.data
        result_delta = []

        for index, data in enumerate(serialized_data):
            if index != 0:
                result_delta.append(
                    (index, serialized_data[index][operation] - serialized_data[index - 1][operation]))
            else:
                result_delta.append(
                    (index, serialized_data[index][operation]))

        return Response(result_delta)


class ProfileCompleteDetailApi(generics.RetrieveAPIView):
    def get_queryset(self):
        pass

    def get(self, request, *args, **kw):
        profile_id = self.kwargs['profile_id']
        queryset = ProfileEngagementMetric.objects.filter(
            profile_id=profile_id, engagement_type=3).first()
        responseData = []
        if queryset:
            responseData = queryset.json_response
        response = Response(responseData, status=status.HTTP_200_OK)
        return response
    '''
    ProfileCompleteDetailApi
    '''
    # serializer_class = PostFilterSerializer
    # model = serializer_class.Meta.model

    # def get_queryset(self):
    #     return []

    # def list(self, request, *args, **kwargs):
    #     import datetime
    #     daysago = datetime.datetime.now() + datetime.timedelta(-10)
    #     daysago = daysago.strftime("%Y-%m-%d")
    #     result = []
    #     sql = '''
    #     SELECT audience_count
    #     FROM public."analyticsApi_profilemetric"
    #     WHERE profile_id = %s ORDER BY created_at DESC LIMIT 1
    #     '''
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql, [self.kwargs['profile_id']])
    #         query_result = cursor.fetchone()
    #         if query_result:
    #             totalFollowerCount = query_result[0]
    #         else:
    #             totalFollowerCount = 0
    #     finally:
    #         cursor.close()

    #     result.append(totalFollowerCount)
    #     sql = '''
    #     SELECT SUM(pm.comment_count) as totalCommentCount,SUM(pm.like_count) as totalLikeCount
    #     FROM public."analyticsApi_postmetric" pm
    #     WHERE pm.profile_id = %s AND pm.is_latest = True
    #     '''
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql, [self.kwargs['profile_id']])
    #         query_result = cursor.fetchone()
    #         totalCommentCount = query_result[0]
    #         totalLikeCount = query_result[1]
    #         result.append(totalCommentCount)
    #         result.append(totalLikeCount)
    #     finally:
    #         cursor.close()

    #     sql = '''
    #     SELECT SUM(a.like_count) as totalLike, SUM(a.comment_count)
    #      as totalComment, SUM(a.engagement_count) as totalEngage
    #      FROM (SELECT  DISTINCT ON (post_id_id)
    #      like_count, engagement_count,comment_count
    #      FROM public."analyticsApi_postmetric"
    #      WHERE profile_id = %s
    #      AND created_at::date = %s) a
    #     '''
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql, [self.kwargs['profile_id'], daysago])
    #         query_result = cursor.fetchone()
    #         if not query_result:
    #             query_result = (0, 0, 0)
    #     finally:
    #         cursor.close()

    #     daysAgoLikeCount = query_result[0]
    #     if not daysAgoLikeCount:
    #         daysAgoLikeCount = 0
    #     daysAgoCommentCount = query_result[1]
    #     if not daysAgoCommentCount:
    #         daysAgoCommentCount = 0
    #     daysAgoEngagementCount = query_result[2]
    #     if not daysAgoEngagementCount:
    #         daysAgoEngagementCount = 0

    #     like = totalLikeCount - daysAgoLikeCount
    #     comment = totalCommentCount - daysAgoCommentCount
    #     result.append(like + comment)

    #     sql = '''
    #     SELECT DISTINCT ON (created_at::date) audience_count
    #     FROM public."analyticsApi_profilemetric"
    #     WHERE profile_id = %s AND created_at::date = %s
    #     ORDER BY created_at::date DESC
    #     '''
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql, [self.kwargs['profile_id'], daysago])
    #         query_result = cursor.fetchone()
    #         if not query_result:
    #             daysAgoFollowerCount = 0
    #         else:
    #             daysAgoFollowerCount = query_result[0]
    #             if not daysAgoFollowerCount:
    #                 daysAgoFollowerCount = 0
    #     finally:
    #         cursor.close()
    #     result.append(totalFollowerCount - daysAgoFollowerCount)
    #     result.append(comment)
    #     result.append(like)

    #     return Response(result)
