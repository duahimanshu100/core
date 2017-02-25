from django.conf.urls import url
from analyticsApi.api.post import PostListApi, PostHistoryListApi
from analyticsApi.api.post import PostFilterUsageApi, PostDistributionApi, PostTagRepartitionApi, PostDetailApi
from analyticsApi.api.post import PostTagUsageApi, PostGeolocationApi, PostDensityApi, PostListApiV2
from analyticsApi.api.engagement import ProfileEngagementHistoryApi, PostMetricListApi, ProfileLikeHistoryApi, ProfileCommentHistoryApi, RecentPostApi, OperationPostApi, FilterImpactLikeApi, FilterImpactCommentApi, HashtagPerformanceApi, EngagementAverageApi, EngagementFrequencyApi, FilterEngagementPostApi, Hour24EngagementApi
from analyticsApi.api.profile import ProfileDetail, ProfileAudiencApi
urlpatterns = [
    url(r'^(?i)api/(?P<profile_id>.+)/Posts$', PostListApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/EngagementAvg$',
        EngagementAverageApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/EngagementFrequency$',
        EngagementFrequencyApi.as_view()),

    url(r'^(?i)api/(?P<profile_id>.+)/Posts/v2$', PostListApiV2.as_view()),
    url(r'^(?i)api/Posts/(?P<post_id>.+)$', PostDetailApi.as_view()),

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
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/ProfileEngagementHistory$',
        ProfileEngagementHistoryApi.as_view()),

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
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/engagement/FilterEngagementPostApi$',
        FilterEngagementPostApi.as_view()),

    url(r'^(?i)api/(?P<post_id>.+)/Posts/engagement/Hour24EngagementApi$',
        Hour24EngagementApi.as_view()),

    url(r'^(?i)api/Profile/(?P<profile_id>.+)$',
        ProfileDetail.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Profile/ProfileAudiencApi$',
        ProfileAudiencApi.as_view()),

]
