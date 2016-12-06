import requests
import json
from datetime import datetime
from analyticsApi.models import SmAccount, Profile, Post, Token
from analyticsApi.utility import Utility
from analyticsApi.serializers import ProfileSerializer, PostSerializer
from analyticsApi.simplyMeasured.api.simplyMeasured import ApiSimplyMeasured


class ApiToken(ApiSimplyMeasured):
    '''
        Apis for simply measured account management
    '''

    # Base url
    BASE_URL = 'refresh-token'

    def __init__(self, token):
        ApiSimplyMeasured.__init__(self)
        self.url = self.url + ApiToken.BASE_URL
        self.headers['Content-Type'] = "application/x-www-form-urlencoded"

    def get_api_token(self):
        token = Token.objects.filter()
        refresh_token = token.refresh_token
        sm_id = token.sm_id
        params = {}
        params['account_id'] = sm_id
        params['refresh_token'] = refresh_token
        params['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        response = self.post()
        if response:
            data = response.content.decode("utf-8")
            data = json.loads(data)
                Token.objects.create(token_type=2, token=data['id_token'])
