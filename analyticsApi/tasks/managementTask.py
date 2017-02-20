# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analyticsApi.models import SmAccount
from analyticsApi.models import SmDataSource
from analyticsApi.serializers import SmAccountSerializer
from analyticsApi.serializers import SmDataSourceSerializer
from analyticsApi.simplyMeasured.api.management.management import ApiManagement
from analyticsApi.utility import Utility
from analyticsApi.simplyMeasured.api.token.token import ApiToken

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJzaW1wbHltZWFzdXJlZC1wcm9kIiwiZGV2aWNlIjoiQnJvd3NlciIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgdXNlcl9pZCB1c2VyX21ldGFkYXRhIiwiZW1haWwiOiJkdWFoaW1hbnNodTEwMEBnbWFpbC5jb20iLCJhcHBfbWV0YWRhdGEiOnsiaXNfc21fYWRtaW4iOmZhbHNlLCJhcGlfYWNjZXNzIjp0cnVlfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6ImR1YWhpbWFuc2h1MTAwQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJIaW1hbnNodSIsImxhc3RfbmFtZSI6IkR1YSJ9LCJhY2NvdW50X2lkIjoiZmQ3YTg0OGEtYmZhOS00YzI0LWI5ZTctYjEwNDllMmQxMzZlIiwicmF0ZWxpbWl0Ijp7Im1vbnRoIjoxMDAwMDAsIm1pbnV0ZSI6NTAwfSwidXNlcl9pZCI6ImF1dGgwfDgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1cGRhdGVkX2F0IjoiMjAxNi0xMi0yMlQxNTo1NTo0MC4wOTBaIiwiaWRlbnRpdGllcyI6W3sidXNlcl9pZCI6IjgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsInByb3ZpZGVyIjoiYXV0aDAiLCJjb25uZWN0aW9uIjoiVUFNREItUHJvZHVjdGlvbiIsImlzU29jaWFsIjpmYWxzZX1dLCJjcmVhdGVkX2F0IjoiMjAxNi0xMS0yNlQxOTowMDo1Ni42NzhaIiwiaXNzIjoiaHR0cHM6Ly9zaW1wbHltZWFzdXJlZC1wcm9kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw4MjIzYTk5Mi0zYWNjLTQ1MTUtODhiZS02MTZkNzNjNjgxN2MiLCJhdWQiOiJQd0RzTDRyUlY3enZHczNoYXdRQXI3NUhabElTaWZLTiIsImV4cCI6MTQ4MjQ2MDYxNywiaWF0IjoxNDgyNDI0NjE3LCJhenAiOiJtU2QzSUIzbnBnelcyNW5HbjBJeHkxU2VMN1YyRUtLRSJ9.Z0cEINHWdEV6nqNuKPUXdaI81SZA0VnM15CU24GnWms'


@shared_task
def syncAccounts():
    '''
    SyncAccounts will create or update the accounts
    of simply measured  associated with the token
    '''
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
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
    api_token = ApiToken()
    TOKEN = api_token.get_api_token()
    if(TOKEN):
        obj = ApiManagement(TOKEN)
        result = obj.get_sm_data_sources()
        result = Utility.save_and_update_data(
            SmDataSourceSerializer, result, SmDataSource, 'ds_id', 'ds_id')
        print(result)
    else:
        print('Token Not Found')
