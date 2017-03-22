from datetime import timedelta, date
from analyticsApi.simplyMeasured.api.token.token import ApiToken
from analyticsApi.models import ProfileMetric, Profile
import requests
import json


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def patchAudienceCount():
    for profile in Profile.objects.filter(is_active=True):
        patchAudienceCountForProfile(str(profile.profile_id))


def patchAudienceCountForProfile(profile_id):
    print('Patching Start for ' + str(profile_id))
    # import pdb
    # pdb.set_trace()
    initial_date = date(2017, 3, 15)
    start_date = date(2017, 3, 16)
    end_date = date(2017, 3, 21)
    last_metric = ProfileMetric.objects.filter(profile_id=profile_id, created_at__year='2017', created_at__month='03', created_at__day='15').order_by('-created_at').first()
    if not last_metric:
        print('Not Found Metric for ' + str(profile_id))
        return
    last_metric = last_metric.audience_count
    # api_token = ApiToken()
    # TOKEN = api_token.get_api_token()
    TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnQiOiJzaW1wbHltZWFzdXJlZC1wcm9kIiwiZGV2aWNlIjoiQnJvd3NlciIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgdXNlcl9pZCB1c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIiwiZW1haWwiOiJkdWFoaW1hbnNodTEwMEBnbWFpbC5jb20iLCJhcHBfbWV0YWRhdGEiOnsiaXNfc21fYWRtaW4iOmZhbHNlLCJhcGlfYWNjZXNzIjp0cnVlfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6ImR1YWhpbWFuc2h1MTAwQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJIaW1hbnNodSIsImxhc3RfbmFtZSI6IkR1YSJ9LCJhY2NvdW50X2lkIjoiZmQ3YTg0OGEtYmZhOS00YzI0LWI5ZTctYjEwNDllMmQxMzZlIiwicmF0ZWxpbWl0Ijp7Im1vbnRoIjozMDAwMDAsIm1pbnV0ZSI6NTAwfSwidXNlcl9pZCI6ImF1dGgwfDgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1cGRhdGVkX2F0IjoiMjAxNy0wMy0yMVQxNTo1MDoxNi45MjBaIiwiaWRlbnRpdGllcyI6W3sidXNlcl9pZCI6IjgyMjNhOTkyLTNhY2MtNDUxNS04OGJlLTYxNmQ3M2M2ODE3YyIsInByb3ZpZGVyIjoiYXV0aDAiLCJjb25uZWN0aW9uIjoiVUFNREItUHJvZHVjdGlvbiIsImlzU29jaWFsIjpmYWxzZX1dLCJjcmVhdGVkX2F0IjoiMjAxNi0xMS0yNlQxOTowMDo1Ni42NzhaIiwiaXNzIjoiaHR0cHM6Ly9zaW1wbHltZWFzdXJlZC1wcm9kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw4MjIzYTk5Mi0zYWNjLTQ1MTUtODhiZS02MTZkNzNjNjgxN2MiLCJhdWQiOiJQd0RzTDRyUlY3enZHczNoYXdRQXI3NUhabElTaWZLTiIsImV4cCI6MTQ5MDE1MzYzMiwiaWF0IjoxNDkwMTE3NjMyLCJhenAiOiJtU2QzSUIzbnBnelcyNW5HbjBJeHkxU2VMN1YyRUtLRSJ9.MQKuwdouKMd_ybG-O_CQly4sllcFl3pZP6ZWu1QKVOA'
    for single_date in daterange(start_date, end_date):  
        analytics_date = single_date.strftime("%Y-%m-%d")
        print ('Calculating the data for ' + str(analytics_date))
        if (TOKEN):
            try:
                url = 'https://api.simplymeasured.com/v1/analytics/fd7a848a-bfa9-4c24-b9e7-b1049e2d136e/profiles/metrics';
                params = {'filter': [
                    'profile.id.eq(' + str(profile_id) + ')',
                    'analytics.timeseries_key.in(' + str(analytics_date) + 'T00:00:01...' + str(analytics_date) + 'T23:59:59)'
                    ],
                    'metrics': 'analytics.audience_count'
                }
                headers = {'content-type': 'application/json'}
                headers['Authorization'] = "Bearer " + TOKEN
                content = requests.get(url,
                            params=params,
                            headers=headers)
                content = content.text
                if content:
                    data = json.loads(content)
                    audience_count = data['data'][0]['attributes']['metrics']['analytics.audience_count']
                    print('Last Audience Count is ' + str(last_metric))
                    last_metric = int(last_metric) + int(audience_count)
                    updated_date = analytics_date.split('-')[-1]
                    print('Updating the record for date ' + str(updated_date))
                    ProfileMetric.objects.filter(profile_id=profile_id, created_at__year='2017', created_at__month='03', created_at__day=updated_date).update(audience_count=last_metric)
                    print('Updated Audience Count is ' + str(last_metric))
                else:
                    print('None')
                    # return vision_results
            except Exception:
                import traceback
                print(traceback.print_exc())
                return {}
        else:
            print('Token Not Found')