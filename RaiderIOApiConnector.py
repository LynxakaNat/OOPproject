import requests

from ApiClient import *


class RaiderIOApiConnector(ApiClient):
    base_url = "https://raider.io"

    def Request(self, url: str, query: dict):
        """
        This function sends the request to raider.io API
        :param url: Full URL of the request
        :param query: What we want to request from RaiderIO
        :return: response in the json form
        """
        response = requests.get(url, params=query)
        response.raise_for_status()
        return response.json()

    def RequestCharacter(self, region: str, realm: str, character: str, field: str = None):
        """
        This function will get us the character information from the raider.io API
        :param region: the region the character is from
        :param realm: the realm the character is from
        :param character: the character's name
        :param field: here you add extra attributes you can request from raider.io about a character. If you want to add
        multiple extra fields you need to seperate them using a comma, for example 'gear,talents,mythic_plus_ranks'
        See https://raider.io/api for the full list of available fields
        :return: a JSON from raiderIO
        """
        url = self.base_url + "/api/v1/characters/profile"
        if field is None:
            params = {'region': region, 'realm': realm, 'name': character}
        else:
            params = {'region': region, 'realm': realm, 'name': character, 'fields': field}
        return self.Request(url,query=params)

    def RequestAffix(self, region: str, locale: str):
        """
        This function will get us the weekly affix information from the raider.io API
        :param region: the region whose affixes you want from
        :param locale: the language in which you want them returned for full list https://raider.io/api
        :return: a JSON from raiderIO
        """
        url = self.base_url + "/api/v1/mythic-plus/affixes"
        params = {'region': region, 'locale': locale}
        return self.Request(url, query=params)

