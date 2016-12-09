import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post, SmToken
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.simplyMeasured.api.simplyMeasured import ApiSimplyMeasured


class ApiToken(ApiSimplyMeasured):
    '''
        Apis for simply measured account management
    '''

    # Base url
    BASE_URL = 'refresh-token'

    def __init__(self):
        ApiSimplyMeasured.__init__(self)
        self.url = self.url + ApiToken.BASE_URL
        self.headers['content-type'] = "application/x-www-form-urlencoded"

    def get_api_token(self, sm_id=None):
        if sm_id:
            token = SmToken.objects.filter(sm_id=sm_id, token_type=1).first()
        else:
            token = SmToken.objects.filter(token_type=1).first()
        refresh_token = token.token
        params = {}
        params['account_id'] = sm_id
        params['refresh_token'] = refresh_token
        params['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        self.payload = params
        response = self.post()
        if response:
            data = response.content.decode("utf-8")
            data = json.loads(data)
            SmToken.objects.create(token_type=2, token=data['id_token'])
