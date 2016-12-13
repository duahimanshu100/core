from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.serializers import PostsListSerializer, PostsFilterUsageSerializer
import dateutil.parser
from django.db.models import Count
from analyticsApi.models import Post
import json
from django.core.serializers.json import DjangoJSONEncoder

class PostListApi(generics.ListAPIView):
    serializer_class = PostsListSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(profile_id=profile_id)
        return queryset.order_by('-created_at')


class PostHistoryListApi(generics.ListAPIView):
    serializer_class = PostsListSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(profile_id=profile_id)
        return queryset.order_by('-created_at')


    def list(self, request, *args, **kwargs):
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


        queryset = queryset.extra({'created_at': "date(created_at)"}).values('created_at').annotate(count=Count('id'))


        serialized = list(queryset)
        return Response(serialized)


class PostFilterUsageApi(generics.ListAPIView):
    serializer_class = PostsFilterUsageSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(profile_id=profile_id)
        return queryset.order_by('-created_at')


    def list(self, request, *args, **kwargs):
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
            queryset = queryset.filter(post_id__created_at__lte=to_date)

        if filter:
            queryset = queryset.filter(post_id__primary_content_type=filter)


        queryset = queryset.values('name').annotate(count=Count('name')).order_by('-count')
        serialized = list(queryset)
        return Response(serialized)