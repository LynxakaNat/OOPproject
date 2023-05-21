from datetime import timedelta, datetime

import discord
import pandas as pd

import ToxicityBot
from ApiConnector import *
import requests

'''client_id = "9932bc5b-bba5-45e8-bfc4-82cf2c4c4877"
secret_key = "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj"
auth_url = "https://www.warcraftlogs.com/oauth/authorize"
token_url = "https://www.warcraftlogs.com/oauth/token"
base_url = "https://www.warcraftlogs.com/api/v2/client"'''


def main():
    connector = ApiConnector("9932bc5b-bba5-45e8-bfc4-82cf2c4c4877", "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj")
    # intents = discord.Intents.default()
    # intents.message_content = True
    #query = """query { reportData { report(code: "bXZK8LBV7Hk4rR2j") {title}} }"""
    #data = ApiConnector.Request(query=query)

    query = """
    query {
     reportData {
      report(code: "vhfX2c9TVPGy7WbN") {rankings(playerMetric : hps)}
      } 
      }
      """
    data = connector.Request(query)
    print(data)
    df = pd.DataFrame(data)
    print(df)

if __name__ == "__main__":
    main()



    # client = ToxicityBot.ToxicityBot(intents=intents)
    # client.run(BOTTOKEN)
