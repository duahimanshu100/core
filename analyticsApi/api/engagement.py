import dateutil.parser
from analyticsApi.serializers import PostMetricSerializer, PostsListSerializer
from django.db.models import Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.utility import Utility
from analyticsApi.models import PostMetric
from django.db import connection
from django.db.models import Max


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
        sql = '''SELECT metric.created_at::date, SUM(metric.like_count) - lag(SUM(metric.like_count)) OVER (ORDER BY metric.created_at::date ASC) as like_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, like_count FROM public."analyticsApi_postmetric" WHERE cast("analyticsApi_postmetric"."profile_id" as bigint) = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at ASC'''
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

    def list(self, request, *args, **kwargs):
        sql = '''SELECT metric.created_at::date, SUM(metric.comment_count) - lag(SUM(metric.comment_count)) OVER (ORDER BY metric.created_at::date ASC) as comment_count FROM ( SELECT DISTINCT ON (created_at::date, post_id_id) created_at, id, comment_count FROM public."analyticsApi_postmetric" WHERE cast("analyticsApi_postmetric"."profile_id" as bigint) = %s ORDER BY created_at::date DESC, post_id_id, created_at DESC) as metric GROUP BY metric.created_at::date ORDER BY created_at ASC'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [self.id])
            result = Utility.dictfetchall(cursor)
            return Response(result)
        finally:
            cursor.close()


class MostRecentPostApi(generics.ListAPIView):
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
        limit_by = int(self.request.query_params.get('limit_by', 5))
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

        queryset = queryset.order_by('-created_at')[:limit_by]
        # post_metrics = PostMetric.objects(post_id__in=queryset, is_latest=True)
        # serializer = PostMetricSerializer(post_metrics, many=True)
        # return Response(serializer.data
        return Response(queryset)
