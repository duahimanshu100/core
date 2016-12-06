# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import Profile, SmAccount
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.simplyMeasured.api.analytics.analytics import ApiAnalytics
from analyticsApi.utility import Utility

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJzaW1wbHltZWFzdXJlZC1wcm9kIiwiZGV2aWNlIjoiQnJvd3NlciIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgdXNlcl9pZCB1c2VyX21ldGFkYXRhIiwiZW1haWwiOiJkdWFoaW1hbnNodTEwMEBnbWFpbC5jb20iLCJhcHBfbWV0YWRhdGEiOnsiaXNfc21fYWRtaW4iOmZhbHNlLCJhcGlfYWNjZXNzIjp0cnVlLCJzbTNfZWxpZ2libGUiOnRydWV9LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiZHVhaGltYW5zaHUxMDBAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkhpbWFuc2h1IiwibGFzdF9uYW1lIjoiRHVhIn0sImFjY291bnRfaWQiOiJmZDdhODQ4YS1iZmE5LTRjMjQtYjllNy1iMTA0OWUyZDEzNmUiLCJyYXRlbGltaXQiOnsibW9udGgiOjEwMDAwMCwibWludXRlIjo1MDB9LCJ1c2VyX2lkIjoiYXV0aDB8ODIyM2E5OTItM2FjYy00NTE1LTg4YmUtNjE2ZDczYzY4MTdjIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVwZGF0ZWRfYXQiOiIyMDE2LTExLTMwVDA3OjIxOjE5LjMxOVoiLCJpZGVudGl0aWVzIjpbeyJ1c2VyX2lkIjoiODIyM2E5OTItM2FjYy00NTE1LTg4YmUtNjE2ZDczYzY4MTdjIiwicHJvdmlkZXIiOiJhdXRoMCIsImNvbm5lY3Rpb24iOiJVQU1EQi1Qcm9kdWN0aW9uIiwiaXNTb2NpYWwiOmZhbHNlfV0sImNyZWF0ZWRfYXQiOiIyMDE2LTExLTI2VDE5OjAwOjU2LjY3OFoiLCJpc3MiOiJodHRwczovL3NpbXBseW1lYXN1cmVkLXByb2QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsImF1ZCI6IlB3RHNMNHJSVjd6dkdzM2hhd1FBcjc1SFpsSVNpZktOIiwiZXhwIjoxNDgwOTk5ODIxLCJpYXQiOjE0ODA5NjM4MjEsImF6cCI6Im1TZDNJQjNucGd6VzI1bkduMEl4eTFTZUw3VjJFS0tFIn0.VfcqwnV0RblqHj-60fTOBJtADuEStMlWDC0R8umX1M0'


@shared_task
def syncProfiles():
    '''
    SyncProfiless will create or update the profiles
    of simply measured  associated with the token and account id
    '''
    obj = ApiAnalytics(TOKEN)
    result = obj.get_profiles()
    r = Utility.save_and_update_data(
        ProfileSerializer, result, Profile, 'profile_id', 'profile_id')
    print(r)


@shared_task
def syncAllProfilesPost():
    '''
    SyncPost will create or update the posts
    of simply measured  associated with the token and profiles
    '''

    for profile in Profile.objects.all():
        syncProfilePosts(profile)


def syncProfilePosts(profile):
    '''
    syncProfilePosts will create or update the posts
    of simply measured  associated with the token and profile
    '''
    params = {'filter': [
        'post.creation_date.gte(2016-01-01)',
        'author.id.eq(' + str(profile.profile_id) + ')']}
    obj = ApiAnalytics(TOKEN)
    print(params)
    obj.get_posts(profile.sm_account.sm_id, params)


def syncSinglePost(post):
    params = {'filter': [
        'post.creation_date.gte(1970-01-01)',
        'author.id.eq(' + str(post.profile_id) + ')',
        'post.id.eq(' + post.post_id + ')'
    ]}
    obj = ApiAnalytics(TOKEN)
    # obj.get_posts_by_profile(profile, None, params)
