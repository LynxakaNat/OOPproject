from datetime import timedelta, datetime

import discord
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from RaiderIOApiConnector import *
from RaiderIOParser import *
BOTTOKEN = "MTEwOTA2NDU2NDE2OTAwMzEwMA.GrlyFw.oSJwLttDBtQ2XMswgAcCwqz_gUuXFUWw_jD31M"   


import ToxicityBot
from WCLApiConnector import *
import requests

from WCLParser import WCLParser

client_id = "9932bc5b-bba5-45e8-bfc4-82cf2c4c4877"
secret_key = "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj"
'''auth_url = "https://www.warcraftlogs.com/oauth/authorize"
token_url = "https://www.warcraftlogs.com/oauth/token"  
base_url = "https://www.warcraftlogs.com/api/v2/client"'''


def main():
    # connector = ApiConnector("9932bc5b-bba5-45e8-bfc4-82cf2c4c4877", "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj")
    # intents = discord.Intents.default()
    # intents.message_content = True
        #query = """query { reportData { report(code: "bXZK8LBV7Hk4rR2j") {title}} }"""
        #data = ApiConnector.Request(query=query)
    client = RaiderIOParser(RaiderIOApiConnector())
    data = client.ParseAffix("eu", "en")
    print(data)

def main3():
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = ToxicityBot.ToxicityBot(intents=intents, command_prefix='!')
    client.run(BOTTOKEN)


def main2():
    WCL = WCLApiConnector(client_id, secret_key)
    # data = WCL.RequestEvent("cVvnhfD3zagRJrTF")
    parser = WCLParser(WCL)
    data = parser.ParseFight("vkMyAmQbKawJhF9B")
    # data = parser.ParseGuild("Memes and Depletes", "Draensor", "EU")
    print(data)
    '''query = """
    query {
     reportData {
      report(code: "YcKV2Mh7WQgLytzJ") {rankings(playerMetric : hps)}
      } 
      }
      """
    data = connector.Request(query)
    # print(data)
    flat_d = pd.json_normalize(data)
    flat_d = pd.json_normalize(flat_d.iloc[0])
    flat_d = pd.json_normalize(flat_d.iloc[0])
    df = pd.DataFrame(flat_d)
    #print(df)
    """with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(df)"""
    healers = df['roles.healers.characters']
    df_healers = pd.DataFrame(healers.iloc[1])
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(df_healers)
    plt.bar(df_healers['name'], df_healers["amount"])
    plt.show()'''

if __name__ == "__main__":
    # main()
    main3()


    # client = ToxicityBot.ToxicityBot(intents=intents)
    # client.run(BOTTOKEN)'''
