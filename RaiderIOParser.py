import pandas as pd

from RaiderIOApiConnector import *


class RaiderIOParser:
    client = None

    def __init__(self, client: RaiderIOApiConnector):
        """

        :param client:
        """
        self.client = client

    def ParseChar(self, region: str, realm: str, character: str, field: str = None) -> pd.Series:
        """

        :param region: the region the character is from
        :param realm: the realm the character is from
        :param character: the character's name
        :param field: here you add extra attributes you can request from raider.io about a character. If you want to add
        multiple extra fields you need to seperate them using a comma, for example 'gear,talents,mythic_plus_ranks'
        See https://raider.io/api for the full list of available fields
        :return: a pandas series containg the information called from a RaiderConnect.RequestCharacter
        """
        char = self.client.RequestCharacter(region, realm, character, field)
        df = pd.Series(char)
        return df

    def ParseAffix(self, region: str, locale: str):
        """

        :param region: the region whose affixes you want from
        :param locale: the language in which you want them returned for full list https://raider.io/api
        :return:
        """
        data = self.client.RequestAffix(region, locale)
        df = pd.Series(data)
        return df
