# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import Profile, SmAccount, ProfileLike, ProfileMetric
from analyticsApi.serializers import ProfileSerializer, PostSerializer, ProfileLikeSerializer,ProfileMetricSerializer
from analyticsApi.simplyMeasured.api.analytics.analytics import ApiAnalytics
from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.token.token import ApiToken
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime


def syncProfiles(is_hourly=False):
    '''
    SyncProfiless will create or update the profiles
    of simply measured  associated with the token and account id
    '''
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    if (TOKEN):
        obj = ApiAnalytics(TOKEN)
        result = obj.get_profiles()
        if result:
            Profile.objects.all().update(is_active=False)

        r = Utility.save_and_update_data(
            ProfileSerializer, result, Profile, 'profile_id', 'profile_id')
        print(r)
        if is_hourly:
            ProfileMetric.objects.filter(is_latest=True).update(is_latest=False)
            Utility.save_and_update_data(ProfileMetricSerializer, result, ProfileMetric)
    else:
        print('Token Not Found')


def syncAllProfilesPost():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    count = 0
    for profile in Profile.objects.filter(is_active=True):
        count = count + 1
        print('Profile Id Sync Starts for ' +
              str(profile.id) + ' at ' + str(datetime.now()))
        syncProfilePosts(profile, TOKEN)
        print('Profile Id Sync Completed for ' +
              str(profile.id) + ' at ' + str(datetime.now()))
        print('Count is ' + str(count))


def syncAllProfilesLikes():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''

    for profile in Profile.objects.filter(is_active=True):
        syncProfileLikes(profile)


def syncProfileLikes(profile):
    '''
    syncProfilePosts will create or update the likes
    of simply measured  associated with the token and profile
    '''
    params = {'filter': [
        # 'post.creation_date.gte(2016-01-01)',
        'author.id.eq(' + str(profile.profile_id) + ')'],
        'dimensions': 'post.creation_date.by(hour)',
        'metrics': 'post.likes_count'
    }
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    if TOKEN:
        obj = ApiAnalytics(TOKEN)
        ret_data = obj.get_profile_likes(
            profile.sm_account.sm_id, profile.profile_id, params)
        r = Utility.save_and_update_data(
            ProfileLikeSerializer, ret_data, ProfileLike, None, None)
        print(r)
    else:
        print('Token Not Found')


def syncProfilePosts(profile, TOKEN):
    '''
    syncProfilePosts will create or update the posts
    of simply measured  associated with the token and profile
    '''
    params = {'filter': [
        'author.id.eq(' + str(profile.profile_id) + ')'],
        'limit': 1000,
        'fields': 'post.url,post.target_url,post.sentiment,post.primary_content_type,post.language,post.province,post.is_brand,post.image_urls,post.distribution_type,post.country,data_source_id,datarank,channel,author.profile_link,author.image_url,author.display_name,post.geo,post.hashtags,post.instagram.image_filter,post.body,post.id,post.content_types,post.creation_date,author.id',
        'metrics': 'post.replies_count,post.shares_count,post.likes_count,post.engagement_total,post.dislikes_count'
    }
    # api_token = ApiToken()
    # TOKEN = api_token.get_api_token()
    if (TOKEN):
        obj = ApiAnalytics(TOKEN)
        # print(params)
        obj.get_posts(profile.sm_account.sm_id, params)
    else:
        print('Token Not Found')


def syncSinglePost(post):
    params = {'filter': [
        'post.creation_date.gte(1970-01-01)',
        'author.id.eq(' + str(post.profile_id) + ')',
        'post.id.eq(' + post.post_id + ')'
    ]}
    obj = ApiAnalytics(TOKEN)
    # obj.get_posts_by_profile(profile, None, params)


@periodic_task(run_every=(crontab(minute=0, hour='*/1')), name="syncAllProfileAndPost", ignore_result=True)
def syncAllProfileAndPost():
    syncProfiles(is_hourly=True)
    syncAllProfilesPost()


@periodic_task(run_every=(crontab()), name="syncAudienceCount", ignore_result=True)
def syncAudienceCount():
    syncProfiles()
