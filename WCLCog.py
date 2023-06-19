import discord
import pandas as pd
from discord.ext import commands
from discord.ext.commands import Bot

from WCLParser import *
import matplotlib.pyplot as plt
from tabulate import *


class WCLCog(commands.Cog):
    parser = None

    def __init__(self, bot: commands.Bot, parser: WCLParser):
        self.bot = bot
        self.parser = parser

    @commands.command()
    async def hps(self, ctx, log):
        """
        This method sends a graph image to discord when an !hps command is invoked
        containing the information about the hps ranking taken from the log
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param log: link to the logged fight
        """
        log = log.split("/")[4]
        data = self.parser.ParseRanking(log, 'hps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.figure()
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'graphs\graph.png')
        await ctx.send(file=discord.File(r'graphs\graph.png'))

    @commands.command()
    async def dps(self, ctx, log):
        """
        This method sends a graph image to discord when a !dps command is invoked
        containing the information about the dps ranking taken from the log
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param log: link to the logged fight
        """
        log = log.split("/")[4]
        data = self.parser.ParseRanking(log, 'dps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.figure()
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'graphs\graph_d.png')
        await ctx.send(file=discord.File(r'graphs\graph_d.png'))

    @commands.command()
    async def kills(self, ctx, log):
        """
        This method sends an embedded discord message when a !kills command is invoked
        containing the information about the amount of bosses that got killed in the log
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param log: link to the logged fight
        """
        log = log.split("/")[4]
        data = self.parser.ParseFight(log)
        data = data[(data['kill'] == True)]
        # we do not type is because it breaks because of pandas
        amount_of_kills = len(data)
        blank_index = [''] * len(data)
        # we add this blank index because we want to make the formatting of the message neater
        data.index = blank_index
        embedded_message = discord.Embed(title="You have killed " + str(amount_of_kills) + " bosses!", description=(
            data['name'].to_string()), color=0x394A8C)
        await ctx.send(embed=embedded_message)

    @commands.command()
    async def wipes(self, ctx, log):
        """
        This method sends an embedded discord message when a !wipes command is invoked
        containing the information about the amount of times players wiped and on what bosses
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param log: link to the logged fight
        """
        log = log.split("/")[4]
        data = self.parser.ParseFight(log)
        data = data[(data['kill'] == False)]
        blank_index = [''] * len(data)
        # we add this blank index because we want to make the formatting of the message neater
        data.index = blank_index
        amount_of_wipes = len(data)
        embedded_message = discord.Embed(title="You have wiped " + str(amount_of_wipes) + " times!", description=(
                data['name'].to_string()), color=0x394A8C)
        await ctx.send(embed=embedded_message)

    @commands.command()
    async def members(self, ctx, guild_name, serv_name, server_reg):
        """
        This method sends an embedded discord message when a !members command is invoked
        containing the information about the amount of players being in a requested guild
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param guild_name: the name of the guild
        :param serv_name: the name of the server of the said guild
        :param server_reg: the name of the region of the server
        """
        data = self.parser.ParseGuild(guild_name, serv_name, server_reg)
        embedded_message = discord.Embed(title="Those are the lovely members of " + guild_name, description=(
                "```" + tabulate(data) + "```"), color=0x394A8C)

        await ctx.send(embed=embedded_message)

    @commands.command()
    async def deaths(self, ctx, log_code):
        """
        This method sends a graph image to discord channel when a !deaths command is invoked
        containing the information about the amount of times players died during the duration
        of the whole raid night (log)
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param log_code: link to the logged fight
        """
        log_code = log_code.split("/")[4]
        fight_id = list(self.parser.ParseFight(log_code).index)
        fight_id = ",".join(map(str, fight_id))
        data_type = "Deaths"
        data = self.parser.ParseEvent(log_code, data_type, fight_id)
        players = self.parser.ParsePlayers(log_code, fight_id)
        for encounter in data['targetID']:
            for player in players['id']:
                if encounter == player:
                    data.loc[data['targetID'] == encounter, 'targetID'] = \
                        players.loc[players['id'] == player, 'name'].iloc[0]

        death = data['targetID'].value_counts()
        samples = death[:6]
        plt.figure()
        plt.bar(samples.index, samples)
        plt.savefig(r'graphs\graph_d.png')

        await ctx.send(file=discord.File(r'graphs\graph_d.png'))
