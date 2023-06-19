import pandas as pd

from WCLApiConnector import *
from Parser import *


class WCLParser(Parser):
    client = None

    def __init__(self, client: WCLApiConnector):
        """
        Initializes the WCL API Parser
        :param client: the WCLApiConnector API client
        """
        self.client = client

    def Parse(self, url: str, query: str):
        """
        This functions sends a request to the WCLApiConnector
        :param url: full URL of the request
        :param query: This is what we want to request from WCL
        :return: It returns the response from the WCL API for the query we gave it
        """
        raw_data = self.client.Request(url, query)
        return raw_data

    def ParseRanking(self, log_code: str, rank_type: str):
        """
        This is the function where we parse the ranking data from the WClApiConnector.RequestRanking
        :param log_code: the code of the log we want the API to read
        :param rank_type: the type of ranking which we want to compare hps/dps
        :return: a pandas dataframe containing the information obtained  from a WClApiConnector.RequestRanking
        """

        raw_data = self.client.RequestRanking(log_code, rank_type)  # this is the data we get from the API
        unpacked_data = raw_data['data']['reportData']['report']['rankings']['data']
        # We now want to transform the data into a proper DataFrame
        parsed_df = pd.DataFrame(unpacked_data).set_index('fightID')
        # We set the index to the fightID in order to be able to clearly differentiate amongst different encounters
        df2 = pd.DataFrame(parsed_df['roles'])
        # -> unpack the dictonaries per fight to a dataframe
        df_final = pd.DataFrame(df2['roles'].iloc[0])
        # Here we are grouping the roles into three individual dataframes so we can then put them in order
        # tanks -> healers -> dps - using pd.concat
        tanks = pd.DataFrame(df_final['tanks']['characters'])
        healers = pd.DataFrame(df_final['healers']['characters'])
        dps = pd.DataFrame(df_final['dps']['characters'])
        frames = [tanks, healers, dps]
        # We set the index to names  in order to be able to use it later in the discord bot input 
        return pd.concat(frames).set_index('name')

    def ParseGuild(self, guild_name: str, serv_name: str, server_reg: str):
        """
        This is the function where we parse the guild data from the WClApiConnector.RequestGuild
        :param guild_name: name of the guild whose members we want to check
        :param serv_name: name of the server of the guild
        :param server_reg: region of the guild server
        :return: a pandas dataframe containing the information obtained from a WClApiConnector.RequestGuild
        """

        raw_data = self.client.RequestGuild(guild_name, serv_name, server_reg)
        unpacked_data = raw_data['data']['guildData']['guild']['members']['data']
        parsed_data = pd.DataFrame(unpacked_data).set_index('name')
        # We set the index to name rather than fightID because it is a neat way for the discord bot input
        parsed_data['faction'] = parsed_data['faction'].apply(lambda x: x['name'])
        # We have to unpack the dictionary of the faction since it has one entry, to make it more readable

        return parsed_data

    def ParseFight(self, log_code: str):
        """
        This is the function where we parse the fight data from the WClApiConnector.RequestFight
        :param log_code: the code of the log we want the API to read
        :return: a pandas dataframe containing the information obtained from a WClApiConnector.RequestFight
        """
        raw_data = self.client.RequestFight(log_code)
        unpacked_data = raw_data['data']['reportData']['report']['fights']
        parsed_df = pd.DataFrame(unpacked_data).set_index('id')
        # We know boss fights are under kill column labeled either True or False
        # Thrash fights are of str None -> so we want to get rid of them to have
        # boss fights
        parsed_df = parsed_df[(parsed_df['kill'] == True) | (parsed_df['kill'] == False)]
        return parsed_df

    def ParseEvent(self, log_code: str, data_type: str, fight_id: str):
        """
        This is the function where we parse the event (encounter) data from the WClApiConnector.RequestEvent.
        This function includes the data from the wipes (unlike ranking)
        :param log_code: the code of the log we want the API to read
        :param data_type: type of the event we want to scrape,
        https://www.warcraftlogs.com/v2-api-docs/warcraft/eventdatatype.doc.html <- for future
        possibility to expand the cog methods
        :param fight_id: the fight encounters we want to analyze the data from
        :return: a pandas dataframe containing the event data obtained from WCLApiConnector.RequestEvent
        """
        raw_data = self.client.RequestEvent(log_code, data_type, fight_id)
        unpacked_data = raw_data['data']['reportData']['report']['events']['data']
        parsed_df = pd.DataFrame(unpacked_data)
        return parsed_df

    def ParsePlayers(self, log_code: str, fight_id: str):
        """
        This is the function where we parse the player details data from the WClApiConnector.RequestPlayers
        :param log_code: the code of the log we want the API to read
        :param fight_id:the fight encounters we want to analyze the data from
        :return: a pandas dataframe containing the player details data obtained from WCLApiConnector.RequestPlayers
        """
        raw_data = self.client.RequestPlayers(log_code, fight_id)
        unpacked_data_dps = raw_data['data']['reportData']['report']['playerDetails']['data']['playerDetails']['dps']
        unpacked_data_heal = raw_data['data']['reportData']['report']['playerDetails']['data']['playerDetails']['healers']
        unpacked_data_tank = raw_data['data']['reportData']['report']['playerDetails']['data']['playerDetails']['tanks']

        dps = pd.DataFrame(unpacked_data_dps)
        heal = pd.DataFrame(unpacked_data_heal)
        tank = pd.DataFrame(unpacked_data_tank)
        frames = [tank, heal, dps]
        # We set the index to names  in order to be able to use it later in the discord bot input
        return pd.concat(frames)
