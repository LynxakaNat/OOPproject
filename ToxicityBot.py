import WCLCog
from WCLParser import *
from RaiderIOCog import *


class ToxicityBot(commands.Bot):
    """
    This is the class of the Toxicity bot, here we initialize and log in the bot
    """
    client_id = None # fill in
    secret_key = None # fill in
    wcl_client = None
    wcl_parser = None
    raider_parser = None
    raider_client = None

    async def on_ready(self):
        """
        This functions log in the bot and adds the functionality of the cogs
        """
        print(f'Logged in as {self.user.name} ({self.user.id})')
        self.wcl_client = WCLApiConnector(self.client_id, self.secret_key)
        self.wcl_parser = WCLParser(self.wcl_client)
        self.raider_client = RaiderIOApiConnector()
        self.raider_parser = RaiderIOParser(self.raider_client)
        await self.add_cog(WCLCog.WCLCog(self, self.wcl_parser))
        await self.add_cog(RaiderIOCog(self, self.raider_parser))

