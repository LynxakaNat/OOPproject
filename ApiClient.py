from abc import *


class ApiClient(ABC):
    base_url = None

    @abstractmethod
    def Request(self, url: str, query):
        # query could be either a dict or a string
        pass
