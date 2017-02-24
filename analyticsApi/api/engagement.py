import dateutil.parser
from analyticsApi.serializers import PostMetricSerializer, PostsListSerializer, PostWithMetricSerializer, PostHashTagSerializer, PostFilterSerializer
from django.db.models import Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.utility import Utility
from analyticsApi.models import PostMetric
from django.db import connection
from django.db.models import Max


class EngagementAverageApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model

    def list(self, request, *args, **kwargs):
        sql = '''SELECT pm.engagement_count, CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' THEN EXTRACT(HOUR FROM post.created_at)::integer ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer END AS "HOUR_OF_POSTING", post.created_at::time, EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=post.post_id) WHERE pm.is_latest=True AND post.profile_id = %s '''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            arr = []
            for i in range(24):
                for j in range(7):
                    arr.append([i, j, 0, 0])

            for row in cursor.fetchall():
                tmp_hour = row[1]
                tmp_day = row[3]
                if(tmp_hour == 24):
                    tmp_hour = 0
                    tmp_day += 1
                    if(tmp_day == 7):
                        tmp_day = 0
                arr[tmp_hour * 7 + tmp_day][2] += 1
                arr[tmp_hour * 7 + tmp_day][3] += row[0]
            for elem in arr:
                tmp = 0
                if elem[2]:
                    tmp = round(elem[3] / elem[2])
                elem.pop()
                elem.pop()
                elem.append(tmp)
            return Response(arr)
        finally:
            cursor.close()


class EngagementFrequencyApi(generics.ListAPIView):
    '''
    Filter impact on like
    '''

    def get_queryset(self):
        return []

    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model

    def list(self, request, *args, **kwargs):
        sql = '''SELECT pm.engagement_count, CASE WHEN post.created_at::time < date_trunc('hour', post.created_at::time) + interval '45 minutes' THEN EXTRACT(HOUR FROM post.created_at)::integer ELSE (EXTRACT(HOUR FROM post.created_at) + 1)::integer END AS "HOUR_OF_POSTING", post.created_at::time, EXTRACT(DOW FROM post.created_at)::integer as dayOfWeek FROM public."analyticsApi_post" post LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=post.post_id) WHERE pm.is_latest=True AND post.profile_id = %s '''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            arr = []
            for i in range(24):
                for j in range(7):
                    arr.append([i, j, 0])

            for row in cursor.fetchall():
                tmp_hour = row[1]
                tmp_day = row[3]
                if(tmp_hour == 24):
                    tmp_hour = 0
                    tmp_day += 1
                    if(tmp_day == 7):
                        tmp_day = 0
                arr[tmp_hour * 7 + tmp_day][2] += 1
            return Response(arr)
        finally:
            cursor.close()


class PostMetricListApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(
            profile_id=profile_id, is_latest=True)
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
        sql = '''SELECT metric.created_at::date, CASE WHEN SUM(metric.like_count) - lag(SUM(metric.like_count)) OVER (ORDER BY metric.created_at::date ASC) > 0 THEN SUM(metric.like_count) - lag(SUM(metric.like_count)) OVER (ORDER BY metric.created_at::date ASC) ELSE 0 END as like_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, like_count FROM public."analyticsApi_postmetric" WHERE profile_id = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at ASC'''
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
        sql = '''SELECT metric.created_at::date, CASE WHEN SUM(metric.comment_count) - lag(SUM(metric.comment_count)) OVER (ORDER BY metric.created_at::date ASC) > 0 THEN SUM(metric.comment_count) - lag(SUM(metric.comment_count)) OVER (ORDER BY metric.created_at::date ASC) ELSE 0 END as comment_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, comment_count FROM public."analyticsApi_postmetric" WHERE profile_id = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at ASC'''
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
            profile_id=profile_id)
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
        post_metrics = PostMetric.objects.filter(
            post_id__in=queryset, is_latest=True)
        serializer = PostWithMetricSerializer(post_metrics, many=True)
        return Response(serializer.data)


class OperationPostApi(generics.ListAPIView):
    '''
    Most and least like
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(
            profile_id=profile_id)
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
        queryset = queryset.filter(is_latest=True)
        # 2016-12-02T17:00:25.910711
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

        order_by_type = '-' if type_of_recent == 'most' else ''
        queryset = queryset.order_by(order_by_type + operation)[:limit_by]
        serializer = PostWithMetricSerializer(queryset, many=True)
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
        sql = '''SELECT pf.name, SUM(comment_count) FROM public."analyticsApi_postfilter" pf LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=pf.post_id_id AND pm.is_latest = TRUE ) LEFT JOIN public."analyticsApi_post" post ON (post.post_id=pf.post_id_id) WHERE pf.profile_id = %s ''' + sql_filter + ''' GROUP BY pf.name'''
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

        sql = '''SELECT pf.name, SUM(like_count) FROM public."analyticsApi_postfilter" pf LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=pf.post_id_id AND pm.is_latest = TRUE ) LEFT JOIN public."analyticsApi_post" post ON (post.post_id=pf.post_id_id) WHERE pf.profile_id = %s '''  + sql_filter +   ''' GROUP BY pf.name'''
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
            ''' FROM public."analyticsApi_posthashtag" ph LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=ph.post_id_id AND pm.is_latest = TRUE ) LEFT JOIN public."analyticsApi_post" post ON (post.post_id=ph.post_id_id) WHERE ph.profile_id = %s ''' + \
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
        SELECT pf.name, sum(pm.engagement_count) as s_e_c 
        FROM public."analyticsApi_postfilter" pf 
        LEFT JOIN public."analyticsApi_postmetric" pm ON (pm.post_id_id=pf.post_id_id AND pm.is_latest = True)
        WHERE pf.profile_id = %s GROUP BY pf.name
        ORDER BY s_e_C DESC
        '''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.kwargs['profile_id']])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()
