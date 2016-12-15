from django.conf.urls import url
from analyticsApi.api.post import PostListApi, PostHistoryListApi
from analyticsApi.api.post import PostFilterUsageApi, PostDistributionApi, PostTagRepartitionApi
from analyticsApi.api.post import PostTagUsageApi, PostGeolocationApi, PostDensityApi
urlpatterns = [
    url(r'^(?i)api/(?P<profile_id>.+)/Posts$', PostListApi.as_view()),

    url(r'^(?i)api/(?P<profile_id>.+)/Posts/History$',
        PostHistoryListApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostFilterUsage$',
        PostFilterUsageApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostTagUsage$',
        PostTagUsageApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostGeolocation$',
        PostGeolocationApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostDensity$', PostDensityApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostDistribution$',
        PostDistributionApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostTagRepartition$',
        PostTagRepartitionApi.as_view())


]