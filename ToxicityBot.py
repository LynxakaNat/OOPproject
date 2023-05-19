from os.path import isfile
from os import environ, makedirs, getcwd

import discord
from discord.ext.commands import Bot, DefaultHelpCommand, bot
from discord import Game
from pathlib import Path
from discord import Intents


class ToxicityBot(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ({self.user.id})')

    async def on_message(self, message):
        print("Hey")

