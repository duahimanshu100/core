from django.conf.urls import url
from analyticsApi.api.post import PostListApi, PostHistoryListApi
from analyticsApi.api.post import PostFilterUsageApi, PostDistributionApi, PostTagRepartitionApi
from analyticsApi.api.post import PostTagUsageApi, PostGeolocationApi, PostDensityApi
from analyticsApi.api.engagement import PostMetricListApi, ProfileLikeHistoryApi, ProfileCommentHistoryApi, RecentPostApi, OperationPostApi, FilterImpactLikeApi, FilterImpactCommentApi, HashtagPerformanceApi
from analyticsApi.api.profile import ProfileDetail,ProfileAudiencApi
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
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostDensity$',
        PostDensityApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostDistribution$',
        PostDistributionApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostTagRepartition$',
        PostTagRepartitionApi.as_view()),

    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/PostMetric$',
        PostMetricListApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/ProfileLikeHistory$',
        ProfileLikeHistoryApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/ProfileCommentHistory$',
        ProfileCommentHistoryApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/RecentPostApi$',
        RecentPostApi.as_view()),

    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/OperationPostApi$',
        OperationPostApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/FilterImpactLikeApi$',
        FilterImpactLikeApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/FilterImpactCommentApi$',
        FilterImpactCommentApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/HashtagPerformanceApi$',
        HashtagPerformanceApi.as_view()),

    url(r'^(?i)api/Profile/(?P<profile_id>.+)$',
        ProfileDetail.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Profile/ProfileAudiencApi$',
        ProfileAudiencApi.as_view()),

]
