import pandas as pd

from RaiderIOApiConnector import *
from Parser import *


class RaiderIOParser(Parser):
    client = None

    def __init__(self, client: RaiderIOApiConnector):
        """

        :param client: the RaiderIOApiConnector client
        """
        self.client = client

    def Parse(self, url: str, query: str):
        data = self.client.Request(url, query)
        df = pd.Series(data)
        return df

    def ParseChar(self, region: str, realm: str, character: str, field: str = None) -> pd.Series:
        """
        This is the function where we parse the character details data from the RaiderIOApiConnector.RequestCharacter
        :param region: the region the character is from
        :param realm: the realm the character is from
        :param character: the character's name
        :param field: here you add extra attributes you can request from raider.io about a character. If you want to add
        multiple extra fields you need to seperate them using a comma, for example 'gear,talents,mythic_plus_ranks'
        See https://raider.io/api for the full list of available fields
        :return: a pandas series containing the information obtained from a RaiderIOApiConnector.RequestCharacter
        """
        char = self.client.RequestCharacter(region, realm, character, field)
        df = pd.Series(char)
        return df

    def ParseAffix(self, region: str, locale: str):
        """
        This is the function where we parse the weekly affix data from the RaiderIOApiConnector.RequestAffix
        :param region: the region whose affixes you want from
        :param locale: the language in which you want them returned for full list https://raider.io/api
        :return: a pandas series containing the data obtained from RaiderConnect.RequestAffix
        """
        data = self.client.RequestAffix(region, locale)
        df = pd.Series(data)
        return df

    def ParseMythicRun(self, season, run_id: str):
        """
        This is the function where we parse a singular mythic dungeon run data
        from the RaiderIOApiConnector.RequestMythicRun
        :param season: name of the season to retrieve (season-df-1, etc.). Defaults to current season.
        :param run_id: ID of the run that you want to get details for
        :return: a pandas series containing the data obtained from RaiderConnect.RequestMythicRun
        """
        data = self.client.RequestMythicRun(season, run_id)
        df = pd.Series(data)
        return df
