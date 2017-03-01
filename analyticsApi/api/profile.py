import dateutil.parser
from analyticsApi.serializers import PostsListSerializer, PostsFilterUsageSerializer, PostsTagUsageSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response
from analyticsApi.models import Profile, ProfileMetric
from django.db.models import Avg


class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    model = serializer_class.Meta.model
    lookup_field = 'profile_id'


class ProfileAudiencApi(generics.ListAPIView):
    '''
    List post filters and post filter count by profile
    '''
    serializer_class = PostsFilterUsageSerializer
    model = ProfileMetric
    paginate_by = 100

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        queryset = self.model.objects.filter(profile_id=profile_id)
        return queryset

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

        queryset = queryset.extra({'created_day': "date(created_at)"}).values(
            'created_day').annotate(count=Avg('audience_count'))
        queryset = queryset.order_by('-created_day')
        serialized = list(queryset)
        return Response(serialized)
