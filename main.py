from datetime import timedelta, datetime
from ApiConnector import *
import requests

client_id = "9932bc5b-bba5-45e8-bfc4-82cf2c4c4877"
secret_key = "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj"
auth_url = "https://www.warcraftlogs.com/oauth/authorize"
token_url = "https://www.warcraftlogs.com/oauth/token"
base_url = "https://www.warcraftlogs.com/api/v2/client"



if __name__ == "__main__":
    connector = ApiConnector("9932bc5b-bba5-45e8-bfc4-82cf2c4c4877","qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj")
