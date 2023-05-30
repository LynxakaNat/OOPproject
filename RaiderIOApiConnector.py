import requests


class RaiderIOApiConnector:
    base_url = "https://raider.io"

    def RequestCharacter(self, region: str, realm: str, character: str, field: str = None):
        '''

        :param region: the region the character is from
        :param realm: the realm the character is from
        :param character: the character's name
        :param field: here you add extra attributes you can request from raider.io about a character. If you want to add
        multiple extra fields you need to seperate them using a comma, for example 'gear,talents,mythic_plus_ranks'
        See https://raider.io/api for the full list of available fields
        :return: a JSON from raiderIO
        '''
        if field is None:
            params = { 'region':region, 'realm':realm, 'name':character}
        else:
            params = {'region': region, 'realm': realm, 'name': character, 'field': field}
        char = requests.get('https://raider.io/api/v1/characters/profile', params=params)
        char.raise_for_status()
        return char.json()
    def RequestAffix(self, region: str, locale :str):
        '''

        :param region: the region whose affixes you want from
        :param locale: the language in which you want them returned for full list https://raider.io/api
        :return: a JSON from raiderIO
        '''
        url = self.base_url + "/api/v1/mythic-plus/affixes"
        params = {'region' : region, 'locale': locale}
        data = requests.get(url, params=params)
        return data.json()