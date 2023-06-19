from abc import ABC, abstractmethod


class Parser(ABC):
    client = None

    @abstractmethod
    def Parse(self, url: str, query: str):
        pass
