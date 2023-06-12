import discord
from discord.ext import commands
from discord.ext.commands import Bot
from RaiderIOParser import *
import matplotlib.pyplot as plt
from tabulate import *


class RaiderIOCog(commands.Cog):
    parser = None

    def __init__(self, bot: commands.Bot, parser: RaiderIOParser):
        self.bot = bot
        self.raider_parser = parser

    @commands.command()
    async def spy(self, ctx, character: str, realm: str, region: str):
        data = self.raider_parser.ParseChar(region, realm, character)
        tit = "We are spying on " + data['name']
        descrp = ""
        if data['faction'] == 'horde':
            descrp = "beautiful"
        else:
            descrp = "filthy"
        embeded_mess = discord.Embed(title=tit, description=
        f"They are a {data['gender']} {data['race']} {data['class']}. They belong to the {descrp} {data['faction']}",
                                     color=0x394A8C)
        embeded_mess.set_thumbnail(url=data['thumbnail_url'])
        await ctx.send(embed=embeded_mess)

    @commands.command()
    async def mythicscore(self, ctx, character: str, realm: str, region: str):
        field = "mythic_plus_scores_by_season:current"
        field2 = "mythic_plus_scores_by_season:previous"
        data = self.raider_parser.ParseChar(region, realm, character, field)
        data2 = self.raider_parser.ParseChar(region, realm, character, field2)
        diff = int(data['mythic_plus_scores_by_season'][0]['segments']['all']['score']) - int(data2['mythic_plus_scores_by_season'][0]['segments']['all']['score'])
        descrp = ""
        if diff >=  0:
            descrp = "increase"
        elif diff < 0:
            descrp = "decrease"
        colour = data["mythic_plus_scores_by_season"][0]['segments']['all']['color']
        sixteen_integer_hex = int(colour.replace("#", ""), 16)
        readable_hex = int(hex(sixteen_integer_hex), 0)
        # https://stackoverflow.com/questions/65402836/discord-py-using-variable-as-discord-embed-color
        embeded_mess = discord.Embed(title=f"This is {data['name']}'s current season's mythic score:",
                                     description=f"{data['mythic_plus_scores_by_season'][0]['segments']['all']['score']}\n"
                                                 f"Compared to the previous season it is a {abs(diff)} points {descrp}",
                                     color=readable_hex)
        await ctx.send(embed=embeded_mess)

    @commands.command()
    async def mythicranking(self, ctx, character: str, realm: str, region: str, spec: str):
        field = "mythic_plus_ranks"
        data = self.raider_parser.ParseChar(region, realm, character, field)

        embeded_mess = discord.Embed(title=f"This is {data['name']}'s ranking score:", color=0x394A8C)
        embeded_mess.add_field(name='Overall:', value=f"> World: {data['mythic_plus_ranks']['overall']['world']}\n>"
                                                      f" Region: {data['mythic_plus_ranks']['overall']['region']}\n>"
                                                      f" Realm: {data['mythic_plus_ranks']['overall']['realm']}")

        embeded_mess.add_field(name=f"{data['class']} class:",
                               value=f"> World: {data['mythic_plus_ranks']['class']['world']}\n>"
                                     f" Region: {data['mythic_plus_ranks']['class']['region']}\n>"
                                     f" Realm: {data['mythic_plus_ranks']['class']['realm']}")
        embeded_mess.add_field(name=f" {data['class']} {spec}  spec:", value=f"> World: {data['mythic_plus_ranks'][f'class_{spec}']['world']}\n>"
                                                      f" Region: {data['mythic_plus_ranks'][f'class_{spec}']['region']}\n>"
                                                      f" Realm: {data['mythic_plus_ranks'][f'class_{spec}']['realm']}")
        await ctx.send(embed=embeded_mess)

    @commands.command()
    async def lastruns(self,ctx, character: str, realm: str, region: str):
        field = "mythic_plus_recent_runs"
        data = self.raider_parser.ParseChar(region, realm, character, field)
        run = 0
        for run in range(3):
            data['mythic_plus_recent_runs'][run]['clear_time_ms'] = str((int(data['mythic_plus_recent_runs'][run]['clear_time_ms']) // 60000))\
                                                                    + ":" + str(int((int(data['mythic_plus_recent_runs'][run]['clear_time_ms']) % 60000) / 1000))
            if int(data['mythic_plus_recent_runs'][run]['num_keystone_upgrades']) > 0:
                data['mythic_plus_recent_runs'][run]['num_keystone_upgrades'] = "yes"
            else:
                data['mythic_plus_recent_runs'][run]['num_keystone_upgrades'] = "no"
            run += 1
        embeded_mess = discord.Embed(title="3 most recent mythic+ runs", color=0x394A8C)
        embeded_mess.add_field(name=f"{data['mythic_plus_recent_runs'][0]['dungeon']}", value=f">Key level: {data['mythic_plus_recent_runs'][0]['mythic_level']}\n>"
                                                                                              f"Clear time: { data['mythic_plus_recent_runs'][0]['clear_time_ms']}\n>"
                                                                                              f"Key timed: {data['mythic_plus_recent_runs'][0]['num_keystone_upgrades']}")
        embeded_mess.add_field(name=f"{data['mythic_plus_recent_runs'][1]['dungeon']}",
                               value=f">Key level: {data['mythic_plus_recent_runs'][1]['mythic_level']}\n>"
                                     f"Clear time: {data['mythic_plus_recent_runs'][1]['clear_time_ms']}\n>"
                                     f"Key timed: {data['mythic_plus_recent_runs'][1]['num_keystone_upgrades']} ")
        embeded_mess.add_field(name=f"{data['mythic_plus_recent_runs'][2]['dungeon']}",
                               value=f">Key level: {data['mythic_plus_recent_runs'][2]['mythic_level']}\n>"
                                     f"Clear time: {data['mythic_plus_recent_runs'][2]['clear_time_ms']}\n>"
                                     f"Key timed: {data['mythic_plus_recent_runs'][2]['num_keystone_upgrades']} ")

        await ctx.send(embed=embeded_mess)
