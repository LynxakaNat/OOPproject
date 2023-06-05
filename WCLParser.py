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
        return df3

