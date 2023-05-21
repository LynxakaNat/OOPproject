from datetime import datetime, timedelta

import requests


# Here we are setting the API
class ApiConnector(object):
    base_url = "https://www.warcraftlogs.com:443/api/v2/client"
    oauth_auth_uri = "https://www.warcraftlogs.com/oauth/authorize"
    token_url = "https://www.warcraftlogs.com/oauth/token"
    current_oauth_token = None
    current_oauth_token_expiry = None
    refresh_time = 86400

    def __init__(self, clientid, secret_key):
        """

        :param clientid: the WCL client ID created when creating an app for WCL
        :param secret_key: the secret key DO NOT SHARE THE KEY
        """

        self.client_id = clientid
        self.secret_key = secret_key
        # Create session

        self.CreateOAuthSession()

    def CreateOAuthSession(self):
        """
        Creates a new OAuth session for WCL
        :return: this function does not return anything
        """
        # Me: hey server my name is Lynx I want to get access
        # Server : hey this is the info now gtfo
        # This allows us to let requests.post take care of the OAuth
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.secret_key))
        # print(response.status_code)
        resp = response.json()
        # print(resp)
        # print(response.headers)
        self.current_oauth_token = resp["access_token"]
        self.current_oauth_token_expiry = (datetime.now() + timedelta(seconds=resp["expires_in"]))

    def RenewToken(self):
        """
        This function checks if the access token has expired or not. If it has we create a new oauth session
        We also refresh if the token is valid for less than one day
        :return: this function does not return anything
        """

        if self.current_oauth_token is None:
            self.CreateOAuthSession()
        elif self.current_oauth_token_expiry is None:
            self.CreateOAuthSession()
        elif (self.current_oauth_token_expiry - datetime.now()).total_seconds() < self.refresh_time:
            self.CreateOAuthSession()
        else:
            return

    def Request(self, query: str):
        """
        :param query: This is what we want to request from WCL
        :return: It returns the response from the WCL API for the query we gave it
        """

        self.RenewToken()  # We always want to check if our access token is not expired.
        url = self.base_url  #
        headers = {"authorization": "Bearer {}".format(self.current_oauth_token),
                   "accept": "application/json"}
        response = requests.get(url, json={'query': query}, headers=headers)

        response.raise_for_status()  # This takes care of some error checking
        return response.json()
