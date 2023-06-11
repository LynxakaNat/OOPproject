import pandas as pd

from WCLApiConnector import *


class WCLParser:
    client = None

    def __init__(self, client: WCLApiConnector):
        self.client = client

    def ParseRanking(self, log_code: str, rank_type:str):
        """

        :param log_code: the code of the log we want the API to read
        :param rank_type: the type of ranking which we want to compare hps/dps
        :return: a pandas series containing the information called from a WClApiConnector.RequestRanking
        """
        
        raw_data = self.client.RequestRanking(log_code, rank_type) # this is the data we get from the API
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

    def ParseGuild(self, guild_name : str, serv_name : str, server_reg : str):
        """

        :param guild_name: name of the guild whose members we want to check
        :param serv_name: name of the server of the guild
        :param server_reg: region of the guild server
        :return: a pandas series containing the information called from a WClApiConnector.RequestGuild
        """

        raw_data = self.client.RequestGuild(guild_name, serv_name, server_reg)
        unpacked_data = raw_data['data']['guildData']['guild']['members']['data']
        parsed_data = pd.DataFrame(unpacked_data).set_index('name')
        # We set the index to name rather than fightID because it is a neat way for the discord bot input
        parsed_data['faction'] = parsed_data['faction'].apply(lambda x: x['name'])
        # We have to unpack the dictionary of the faction since it has one entry, to make it more readable
        
        return parsed_data
    
    def ParseFight(self, log_code : str):
        """

        :param log_code: the code of the log we want the API to read
        :return:  pandas series containing the information called from a WClApiConnector.RequestFight
        """
        raw_data = self.client.RequestFight(log_code)
        unpacked_data = raw_data['data']['reportData']['report']['fights']
        parsed_df = pd.DataFrame(unpacked_data).set_index('id')
        # We know boss fights are under kill column labeled either True or False
        # Thrash fights are of str None -> so we want to get rid of them to have
        # boss fights
        parsed_df = parsed_df[(parsed_df['kill'] == True)| (parsed_df['kill'] == False)]
        return parsed_df 
   