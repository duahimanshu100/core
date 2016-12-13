from django.conf.urls import url
from analyticsApi.api.post import PostListApi,PostHistoryListApi,PostFilterUsageApi
urlpatterns = [
    url(r'^(?i)api/(?P<profile_id>.+)/Posts$', PostListApi.as_view()),

    url(r'^(?i)api/(?P<profile_id>.+)/Posts/History$', PostHistoryListApi.as_view()),
    url(r'^(?i)api/(?P<profile_id>.+)/Posts/PostFilterUsage$', PostFilterUsageApi.as_view()),

    ]