import dateutil.parser
from analyticsApi.serializers import PostMetricSerializer
from django.db.models import Case, When
from django.db.models import Count
from django.db.models import IntegerField, Sum,Avg
from django.db.models.functions import Extract
from rest_framework import generics
from rest_framework.response import Response


class PostMetricListApi(generics.ListAPIView):
    '''
    List post and post count by profile
    '''
    serializer_class = PostMetricSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(profile_id=profile_id,is_latest=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        queryset = queryset.aggregate(avg_like=Avg('like_count'),
                                      avg_comment=Avg('comment_count'),
                                      total_like=Sum('like_count'),
                                      total_comment=Sum('comment_count'),
                                      )
        return Response(queryset)
