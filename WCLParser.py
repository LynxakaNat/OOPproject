import pandas as pd

from WCLApiConnector import *


class WCLParser:
    client = None

    def __init__(self, client: WCLApiConnector):
        self.client = client

    def ParseRanking(self, log_code: str, rank_type:str):
        query = """
            query {
             reportData {
              report(code: \"""" + log_code + """\") {rankings(playerMetric : """+rank_type+""")
                    }
                } 
              }"""
        data = self.client.Request(self.client.base_url, query)
        # print(data)
        data2 = data['data']['reportData']['report']['rankings']['data']
        df = pd.DataFrame(data2).set_index('fightID')
        df2 = pd.DataFrame(df['roles'])
        df3 = pd.DataFrame(df2['roles'].iloc[0])
        healers = pd.DataFrame(df3['healers']['characters'])
        tanks = pd.DataFrame(df3['tanks']['characters'])
        dps = pd.DataFrame(df3['dps']['characters'])
        frames = [tanks, healers, dps]
        return pd.concat(frames).set_index('name')

    def ParseGuild(self, guild_name : str, serv_name : str, server_reg : str):
        query = """
            query {
             guildData {
              guild(name: \"""" + guild_name + """\", serverSlug: \"""" + serv_name + """\", serverRegion: \"""" + server_reg + """\"){
              members { data {name level faction {name}}} 
              }
                    }
              }
              """
        data = self.client.Request(self.client.base_url, query)
        data2 = data['data']['guildData']['guild']['members']['data']
        data3 = pd.DataFrame(data2).set_index('name')
        data3['faction'] = data3['faction'].apply(lambda x: x['name'])
        
        return data3
