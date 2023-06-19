from datetime import datetime, timedelta

import requests
from ApiClient import *


# Here we are setting the API
class WCLApiConnector(ApiClient):
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
        # This allows us to let requests.post take care of the OAuth
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.secret_key))
        resp = response.json()
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

    def Request(self, url: str, query: str):
        """
        :param url: full URL of the request
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

    def RequestGuild(self, guild_name: str, serv_name: str, server_reg: str):
        """
        This function sends the guild request to the WCL API
        :param guild_name: name of the guild whose members we want to check
        :param serv_name: name of the server of the guild
        :param server_reg: region of the guild server
        :return: It returns the response from the WCL API for the guild query we gave it
        """

        query = """
            query {
             guildData {
              guild(name: \"""" + guild_name + """\", serverSlug: \"""" + serv_name + """\", serverRegion: \"""" + server_reg + """\"){
              members { data {name level faction {name}}} 
              }
                    }
              }
              """
        data = self.Request(self.base_url, query)
        return data

    def RequestRanking(self, log_code: str, rank_type: str):
        """
        This function sends the selected ranking request to the WCL API
        :param log_code: the code of the log we want the API to read
        :param rank_type: the type of ranking which we want to compare hps/dps
        :return: returns the response from the WCL API for the ranking query we gave it
        """

        query = """
            query {
             reportData {
              report(code: \"""" + log_code + """\") {rankings(playerMetric : """ + rank_type + """)
                    }
                } 
              }"""

        data = self.Request(self.base_url, query)
        return data

    def RequestFight(self, log_code: str):
        """
        This function sends the selected encounter request to the WCL API
        :param log_code:  the code of the log we want the API to read
        :return: returns the response from the WCL API for the fight query we gave it
        """
        query = """
            query {
             reportData {
              report(code: \"""" + log_code + """\") {fights {  
                id
                name    
                bossPercentage
                averageItemLevel
                difficulty
                encounterID
                endTime
                fightPercentage
                kill
                 }
            }
                    }

              }"""
        data = self.Request(self.base_url, query)
        return data

    def RequestEvent(self, log_code: str, data_type: str, fight_id: str):
        """
        This function sends the selected event request to the WCL API
        :param log_code:  the code of the log we want the API to read
        :param data_type: type of the event we want to scrape,
        https://www.warcraftlogs.com/v2-api-docs/warcraft/eventdatatype.doc.html <- for future
        possibility to expand the cog methods
        :param fight_id: the fight encounters we want to analyze the data from
        :return: returns the response from the WCL API for the event query we gave it
        """
        query = """
                                    query { 
                                        reportData {
                                            report(code: \"""" + log_code + """\") {
                                                events(dataType: """ + data_type + """ fightIDs: 
                                                [""" + fight_id + """] limit: 10000){ data } } } }"""
        return self.Request(self.base_url, query)

    def RequestPlayers(self, log_code: str, fight_id: str):
        """
        This function sends the player details request to the WCL API
        :param log_code:  the code of the log we want the API to read
        :param fight_id: the fight encounters we want to analyze the data from
        :return: returns the response from the WCL API for the event query we gave it
        """
        query = """
                                            query { 
                                                reportData {
                                                    report(code: \"""" + log_code + """\") {
                                                        playerDetails(fightIDs: [""" + fight_id + """])
                                                    }
                                                } 
                                            }
                                            """
        return self.Request(self.base_url, query)
