from os.path import isfile
from os import environ, makedirs, getcwd

import discord
from discord.ext.commands import Bot, DefaultHelpCommand, bot
from discord import Game
from pathlib import Path
from discord import Intents
from WCLApiConnector import *
import WCLCog
from WCLParser import *
from discord.ext import commands

class ToxicityBot(commands.Bot):
    client_id = "9932bc5b-bba5-45e8-bfc4-82cf2c4c4877"
    secret_key = "qvukkWRBpLLgumxlFrP82zC8mEeDLmFeoPcIXgdj"
    client = None
    parser = None
    

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')
        self.client = WCLApiConnector(self.client_id, self.secret_key)
        self.parser = WCLParser(self.client)
        await self.add_cog(WCLCog.WCLCog(self, self.parser))

    '''async def on_message(self, message):
        print("Hey")'''

