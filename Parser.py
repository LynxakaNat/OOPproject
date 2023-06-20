from abc import ABC, abstractmethod


class Parser(ABC):
    client = None

    @abstractmethod
    def Parse(self, url: str, query: str):
        """
        This function would parse the data from the respective API

        :param url: full URL of the request
        :param query: This is what we want to request from WCL
        :return: It returns nothing since it's an abstract class
        """
        pass
