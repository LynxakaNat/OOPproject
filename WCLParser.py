from ApiConnector import *


class WCLParser:
    wcl_client = None

    def __init__(self, client):
        self.wcl_client = client
