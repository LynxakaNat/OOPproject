import discord
from discord.ext import commands
from discord.ext.commands import Bot    
from WCLParser import * 
import matplotlib.pyplot as plt
class WCLCog(commands.Cog):
    parser = None

    def __init__(self, bot : commands.Bot, parser : WCLParser):
        self.bot = bot 
        self.parser = parser

    '''@commands.Cog.listener()'''
    '''async def on_message(self, message):
        channel = message.guild.system_channel
        if channel is not None and message.author != self.bot.user:
            await channel.send('ME LIKEY KITTIES')'''


    @commands.command()
    async def hps(self, ctx, log):
        data = self.parser.ParseRanking(log, 'hps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'C:\Users\zycho\Desktop\oop\OOPproject\graphs\graph.png')
        await ctx.send(file=discord.File(r'C:\Users\zycho\Desktop\oop\OOPproject\graphs\graph.png'))

    @commands.command()
    async def dps(self, ctx, log):
        data = self.parser.ParseRanking(log, 'dps')
        sorted_data = data.sort_values('amount', ascending=False)
        samples = sorted_data[:5]
        plt.bar(samples.index, samples['amount'])
        plt.savefig(r'C:\Users\zycho\Desktop\oop\OOPproject\graphs\graph.png')
        await ctx.send(file=discord.File(r'C:\Users\zycho\Desktop\oop\OOPproject\graphs\graph.png'))

    @commands.command()
    async def kills(self, ctx, log):
        data = self.parser.ParseFight(log)
    
        data = data[(data['kill'] == True)]
        amount = len(data)
        embeded_mess = discord.Embed(title="You have killed " + str(amount) + " bosses!", description=(data['name'].to_string()), color=0x394A8C)
        await ctx.send(embed=embeded_mess)
