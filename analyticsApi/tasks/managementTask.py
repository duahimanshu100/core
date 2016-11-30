# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import SmAccount
from analyticsApi.models import SmDataSource
from analyticsApi.serializers import SmAccountSerializer
from analyticsApi.serializers import SmDataSourceSerializer
from analyticsApi.apiSimplyMeasured import ApiManagement
from analyticsApi.utility import Utility

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJzaW1wbHltZWFzdXJlZC1wcm9kIiwiZGV2aWNlIjoiQnJvd3NlciIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgdXNlcl9pZCB1c2VyX21ldGFkYXRhIiwiZW1haWwiOiJkdWFoaW1hbnNodTEwMEBnbWFpbC5jb20iLCJhcHBfbWV0YWRhdGEiOnsiaXNfc21fYWRtaW4iOmZhbHNlLCJhcGlfYWNjZXNzIjp0cnVlLCJzbTNfZWxpZ2libGUiOnRydWV9LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiZHVhaGltYW5zaHUxMDBAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkhpbWFuc2h1IiwibGFzdF9uYW1lIjoiRHVhIn0sImFjY291bnRfaWQiOiJmZDdhODQ4YS1iZmE5LTRjMjQtYjllNy1iMTA0OWUyZDEzNmUiLCJyYXRlbGltaXQiOnsibW9udGgiOjEwMDAwMCwibWludXRlIjo1MDB9LCJ1c2VyX2lkIjoiYXV0aDB8ODIyM2E5OTItM2FjYy00NTE1LTg4YmUtNjE2ZDczYzY4MTdjIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVwZGF0ZWRfYXQiOiIyMDE2LTExLTMwVDA3OjIxOjE5LjMxOVoiLCJpZGVudGl0aWVzIjpbeyJ1c2VyX2lkIjoiODIyM2E5OTItM2FjYy00NTE1LTg4YmUtNjE2ZDczYzY4MTdjIiwicHJvdmlkZXIiOiJhdXRoMCIsImNvbm5lY3Rpb24iOiJVQU1EQi1Qcm9kdWN0aW9uIiwiaXNTb2NpYWwiOmZhbHNlfV0sImNyZWF0ZWRfYXQiOiIyMDE2LTExLTI2VDE5OjAwOjU2LjY3OFoiLCJpc3MiOiJodHRwczovL3NpbXBseW1lYXN1cmVkLXByb2QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsImF1ZCI6IlB3RHNMNHJSVjd6dkdzM2hhd1FBcjc1SFpsSVNpZktOIiwiZXhwIjoxNDgwNTI2NjIyLCJpYXQiOjE0ODA0OTA2MjIsImF6cCI6Im1TZDNJQjNucGd6VzI1bkduMEl4eTFTZUw3VjJFS0tFIn0.Sj90j-yGbSND6yrciAj-nhve6aO4GUf3z0UtC8X7A8g'


@shared_task
def syncAccounts():
    '''
    SyncAccounts will create or update the accounts
    of simply measured  associated with the token
    '''
    obj = ApiManagement(TOKEN)
    result = obj.get_sm_accounts()
    r = Utility.save_and_update_data(
        SmAccountSerializer, result, SmAccount, 'sm_id', 'sm_id')
    print(r)


def syncDataSources():
    '''
    SyncDataSources will create or update the dataSources
    of simply measured  associated with the token
    '''
    obj = ApiManagement(TOKEN)
    result = obj.get_sm_data_sources()
    result = Utility.save_and_update_data(
        SmDataSourceSerializer, result, SmDataSource, 'ds_id', 'ds_id')
    print(result)
