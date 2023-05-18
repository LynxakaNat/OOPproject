from datetime import datetime, timedelta

import requests

# Here we are setting the API
class ApiConnector(object):
    def __init__(self,clientid, secret_key):
        self.client_id = clientid
        self.secret_key = secret_key
        self.baseURL = "https://www.warcraftlogs.com:443/api/v2/client"

        self.oauth_auth_uri = "https://www.warcraftlogs.com/oauth/authorize"
        self.token_url = "https://www.warcraftlogs.com/oauth/token"
        self.oauth_session = None
        self.current_oauth_token = None
        self.current_oauth_token_expiry = None
        # Create session

        self.CreateOauthSession()

    def CreateOauthSession(self):
        # Me: hey server my name is Lynx I want to get access
        # Server : hey this is the info now gtfo
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.secret_key))
        print(response.status_code)
        resp = response.json()
        # print(resp)
        print(response.headers)
        self.current_oauth_token = resp["access_token"]
        self.current_oauth_token_expiry = (datetime.now() + timedelta(seconds=resp["expires_in"]))

