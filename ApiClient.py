from abc import *


class ApiClient(ABC):
    base_url = None

    @abstractmethod
    def Request(self, url: str, query):
        """
        This function sends the request into the respective API Connector

        :param url: full URL of the request
        :param query: This is what we want to request from WCL
        :return: It returns nothing since it's an abstract class
        """
        # query could be either a dict or a string
        pass
