# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import Profile, SmAccount, ProfileLike
from analyticsApi.serializers import ProfileSerializer, PostSerializer, ProfileLikeSerializer
from analyticsApi.simplyMeasured.api.analytics.analytics import ApiAnalytics
from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.token.token import ApiToken
from celery.task.schedules import crontab
from celery.decorators import periodic_task

# TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJzaW1wbHltZWFzdXJlZC1wcm9kIiwiZGV2aWNlIjoiQnJvd3NlciIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgdXNlcl9pZCB1c2VyX21ldGFkYXRhIiwiZW1haWwiOiJkdWFoaW1hbnNodTEwMEBnbWFpbC5jb20iLCJhcHBfbWV0YWRhdGEiOnsiaXNfc21fYWRtaW4iOmZhbHNlLCJhcGlfYWNjZXNzIjp0cnVlfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6ImR1YWhpbWFuc2h1MTAwQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJIaW1hbnNodSIsImxhc3RfbmFtZSI6IkR1YSJ9LCJhY2NvdW50X2lkIjoiZmQ3YTg0OGEtYmZhOS00YzI0LWI5ZTctYjEwNDllMmQxMzZlIiwicmF0ZWxpbWl0Ijp7Im1vbnRoIjoxMDAwMDAsIm1pbnV0ZSI6NTAwfSwidXNlcl9pZCI6ImF1dGgwfDgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1cGRhdGVkX2F0IjoiMjAxNi0xMi0xNVQwNjoyNDoxMS42OTBaIiwiaWRlbnRpdGllcyI6W3sidXNlcl9pZCI6IjgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsInByb3ZpZGVyIjoiYXV0aDAiLCJjb25uZWN0aW9uIjoiVUFNREItUHJvZHVjdGlvbiIsImlzU29jaWFsIjpmYWxzZX1dLCJjcmVhdGVkX2F0IjoiMjAxNi0xMS0yNlQxOTowMDo1Ni42NzhaIiwiaXNzIjoiaHR0cHM6Ly9zaW1wbHltZWFzdXJlZC1wcm9kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw4MjIzYTk5Mi0zYWNjLTQ1MTUtODhiZS02MTZkNzNjNjgxN2MiLCJhdWQiOiJQd0RzTDRyUlY3enZHczNoYXdRQXI3NUhabElTaWZLTiIsImV4cCI6MTQ4MjQ1NTg2OSwiaWF0IjoxNDgyNDE5ODY5LCJhenAiOiJtU2QzSUIzbnBnelcyNW5HbjBJeHkxU2VMN1YyRUtLRSJ9.awZ3ijvb1r7fKRJZAQPh1H6L7OiUdKRnZ32CHveKocU'


@shared_task
def syncProfiles():
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
    else:
        print('Token Not Found')


# @periodic_task(run_every=(crontab(minute='*/60')), name="syncAllProfilesPost", ignore_result=True)
def syncAllProfilesPost():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''

    for profile in Profile.objects.filter(is_active=True):
        syncProfilePosts(profile)


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
    obj = ApiAnalytics(TOKEN)
    ret_data = obj.get_profile_likes(
        profile.sm_account.sm_id, profile.profile_id, params)
    r = Utility.save_and_update_data(
        ProfileLikeSerializer, ret_data, ProfileLike, None, None)
    print(r)


def syncProfilePosts(profile):
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
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
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
