from analyticsApi.serializers import PostMetricSerializer
from django.db.models import Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.utility import Utility
from django.db import connection


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
