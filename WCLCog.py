import discord
from discord.ext import commands
from discord.ext.commands import Bot
from WCLParser import *
import matplotlib.pyplot as plt
from tabulate import *


class WCLCog(commands.Cog):
    wcl_parser = None

    def __init__(self, bot: commands.Bot, parser: WCLParser):
        self.bot = bot
        self.wcl_parser = parser

    @commands.command()
    async def hps(self, ctx, log):
        data = self.wcl_parser.ParseRanking(log, 'hps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'graphs\graph.png')
        await ctx.send(file=discord.File(r'graphs\graph.png'))

    @commands.command()
    async def dps(self, ctx, log):
        data = self.wcl_parser.ParseRanking(log, 'dps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'graphs\graph.png')
        await ctx.send(file=discord.File(r'graphs\graph.png'))

    @commands.command()
    async def kills(self, ctx, log):
        data = self.wcl_parser.ParseFight(log)

        data = data[(data['kill'] == True)]
        amount = len(data)
        blank_index = [''] * len(data)
        data.index = blank_index
        embeded_mess = discord.Embed(title="You have killed " + str(amount) + " bosses!", description=(
            data['name'].to_string()), color=0x394A8C)
        await ctx.send(embed=embeded_mess)

    @commands.command()
    async def wipes(self, ctx, log):
        data = self.wcl_parser.ParseFight(log)
        data = data[(data['kill'] == False)]
        blank_index = [''] * len(data)
        data.index = blank_index
        amount = len(data)
        embeded_mess = discord.Embed(title="You have wiped " + str(amount) + " times!", description=(
                "```" + data['name'].to_string() + "```"), color=0x394A8C)
        await ctx.send(embed=embeded_mess)

    @commands.command()
    async def members(self, ctx, guild_name, serv_name, server_reg):
        data = self.wcl_parser.ParseGuild(guild_name, serv_name, server_reg)
        embeded_mess = discord.Embed(title="Those are the lovely members of " + guild_name, description=(
                "```" + tabulate(data) + "```"), color=0x394A8C)

        await ctx.send(embed=embeded_mess)
