import discord
from discord.ext import commands
from RaiderIOParser import *


# This is the discord cog class for the RaiderIO data
# This class already inherits the commands.Cog metaclass
class RaiderIOCog(commands.Cog):
    parser = None

    def __init__(self, bot: commands.Bot, parser: RaiderIOParser):
        """
        Here we initialize the RaiderIOCog

        :param bot: the Toxicity bot
        :param parser: the RaiderIOParser
        """
        self.bot = bot
        self.parser = parser

    @commands.command()
    async def spy(self, ctx, character: str, realm: str, region: str):
        """
        This method sends an embedded discord message when a !spy command is invoked
        containing the basic information about the requested character

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param character: the name of the character we want to grab the data about
        :param realm: the name of the server of the said character
        :param region: the name of the region of the server
        """
        data = self.parser.ParseChar(region, realm, character)
        title_message = "We are spying on " + data['name']
        if data['faction'] == 'horde':
            adjective = "beautiful"
        else:
            adjective = "filthy"
        embedded_message = discord.Embed(title=title_message, description=f"They are a {data['gender']} "
                                                                          f"{data['race']} {data['class']}. "
                                                                          f"They belong to the {adjective} "
                                                                          f"{data['faction']}",
                                         color=0x394A8C)
        embedded_message.set_thumbnail(url=data['thumbnail_url'])
        await ctx.send(embed=embedded_message)

    @commands.command()
    async def mythicscore(self, ctx, character: str, realm: str, region: str):
        """
        This method sends an embedded discord message when a !mythicscore command is invoked
        containing the mythic score information about the requested character

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param character: the name of the character we want to grab the data about
        :param realm: the name of the server of the said character
        :param region: the name of the region of the server
        """
        field_current_szn = "mythic_plus_scores_by_season:current"
        field_previous_szn = "mythic_plus_scores_by_season:previous"
        data_current_szn = self.parser.ParseChar(region, realm, character, field_current_szn)
        data_previous_szn = self.parser.ParseChar(region, realm, character, field_previous_szn)
        difference = int(data_current_szn['mythic_plus_scores_by_season'][0]['segments']['all']['score']) - int(
            data_previous_szn['mythic_plus_scores_by_season'][0]['segments']['all']['score'])
        adjective = ""
        if difference >= 0:
            adjective = "increase"
        elif difference < 0:
            adjective = "decrease"
        # Here we want to make the colour of the embedded message be able to change
        # depending on the mythic score
        colour = data_current_szn["mythic_plus_scores_by_season"][0]['segments']['all']['color']
        sixteen_integer_hex = int(colour.replace("#", ""), 16)
        readable_hex = int(hex(sixteen_integer_hex), 0)
        # https://stackoverflow.com/questions/65402836/discord-py-using-variable-as-discord-embed-color
        embedded_message = discord.Embed(title=f"This is {data_current_szn['name']}'s current season's mythic score:",
                                         description=f"{data_current_szn['mythic_plus_scores_by_season'][0]['segments']['all']['score']}\n"
                                                     f"Compared to the previous season "
                                                     f"it is a {abs(difference)} points {adjective}",
                                         color=readable_hex)
        await ctx.send(embed=embedded_message)

    @commands.command()
    async def mythicranking(self, ctx, character: str, realm: str, region: str, spec: str):
        """
        This method sends an embedded discord message when a !mythicranking command is invoked
        containing the mythic ranking information (world,region, realm) about the requested character

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param character: the name of the character we want to grab the data about
        :param realm: the name of the server of the said character
        :param region: the name of the region of the server
        :param spec: the role character is playing (healer, tank, dps)
        :return:
        """
        field = "mythic_plus_ranks"
        data = self.parser.ParseChar(region, realm, character, field)

        embedded_message = discord.Embed(title=f"This is {data['name']}'s ranking score:", color=0x394A8C)
        embedded_message.add_field(name='Overall:', value=f"> World: {data['mythic_plus_ranks']['overall']['world']}\n>"
                                                          f" Region: {data['mythic_plus_ranks']['overall']['region']}\n>"
                                                          f" Realm: {data['mythic_plus_ranks']['overall']['realm']}")

        embedded_message.add_field(name=f"{data['class']} class:",
                                   value=f"> World: {data['mythic_plus_ranks']['class']['world']}\n>"
                                         f" Region: {data['mythic_plus_ranks']['class']['region']}\n>"
                                         f" Realm: {data['mythic_plus_ranks']['class']['realm']}")
        embedded_message.add_field(name=f" {data['class']} {spec}  spec:",
                                   value=f"> World: {data['mythic_plus_ranks'][f'class_{spec}']['world']}\n>"
                                         f" Region: {data['mythic_plus_ranks'][f'class_{spec}']['region']}\n>"
                                         f" Realm: {data['mythic_plus_ranks'][f'class_{spec}']['realm']}")
        await ctx.send(embed=embedded_message)

    @commands.command()
    async def lastruns(self, ctx, character: str, realm: str, region: str):
        """
        This method sends an embedded discord message when a !lastruns command is invoked
        containing the information about three most recent runs of mythic dungeons done
        by the requested character

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param character: the name of the character we want to grab the data about
        :param realm: the name of the server of the said character
        :param region: the name of the region of the server
        """
        field = "mythic_plus_recent_runs"
        data = self.parser.ParseChar(region, realm, character, field)
        embedded_message = discord.Embed(title="3 most recent mythic+ runs", color=0x394A8C)

        for run in range(3):
            run_data = data['mythic_plus_recent_runs'][run]
            clear_time_ms = int(run_data['clear_time_ms'])
            clear_time_formatted = f"{clear_time_ms // 60000}:{(clear_time_ms % 60000) // 1000}"

            if int(run_data['num_keystone_upgrades']) > 0:
                num_keystone_upgrades = "yes"
            else:
                num_keystone_upgrades = "no"

            embedded_message.add_field(
                name=run_data['dungeon'],
                value=f"> Key level: {run_data['mythic_level']}\n"
                      f"> Clear time: {clear_time_formatted}\n"
                      f"> Key timed: {num_keystone_upgrades}")

        await ctx.send(embed=embedded_message)

    @commands.command()
    async def bestruns(self, ctx, character: str, realm: str, region: str):
        """
        This method sends an embedded discord message when a !bestruns command is invoked
        containing the information about three best runs of mythic dungeons done
        by the requested character

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param character: the name of the character we want to grab the data about
        :param realm: the name of the server of the said character
        :param region: the name of the region of the server
        """
        field = "mythic_plus_best_runs"
        data = self.parser.ParseChar(region, realm, character, field)
        embedded_message = discord.Embed(title="3 best mythic+ runs", color=0x394A8C)

        for run in range(3):
            clear_time = int(data['mythic_plus_best_runs'][run]['clear_time_ms'])
            minutes = clear_time // 60000
            seconds = (clear_time % 60000) / 1000

            data['mythic_plus_best_runs'][run]['clear_time_ms'] = f"{minutes}:{seconds}"
            if int(data['mythic_plus_best_runs'][run]['num_keystone_upgrades']) > 0:
                data['mythic_plus_best_runs'][run]['num_keystone_upgrades'] = "yes"
            else:
                data['mythic_plus_best_runs'][run]['num_keystone_upgrades'] = "no"

            embedded_message.add_field(
                name=f"{data['mythic_plus_best_runs'][run]['dungeon']}",
                value=f">Key level: {data['mythic_plus_best_runs'][run]['mythic_level']}\n"
                      f">Clear time: {data['mythic_plus_best_runs'][run]['clear_time_ms']}\n"
                      f">Key timed: {data['mythic_plus_best_runs'][run]['num_keystone_upgrades']}\n"
                      f">Main affix: {data['mythic_plus_best_runs'][run]['affixes'][0]['name']}")

        await ctx.send(embed=embedded_message)

    @commands.command()
    async def affix(self, ctx, region: str, locale: str = None):
        """
        This method sends an embedded discord message when an !affix command is invoked
        containing the information about the region's affixes
        
        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param region: the name of the region of the server
        :param locale: the language in which you want them returned for full list https://raider.io/api
        defaults to english
        """
        if locale is None:
            data = self.parser.ParseAffix(region, "en")
        else:
            data = self.parser.ParseAffix(region, locale)
        embedded_message = discord.Embed(title="This week's affixes are:", color=0x394A8C)
        for affix in range(3):
            embedded_message.add_field(name=f"{data['affix_details'][affix]['name']}",
                                       value=f"Description: {data['affix_details'][affix]['description']}")

        await ctx.send(embed=embedded_message)

    @commands.command()
    async def run(self, ctx, run_id: str, season: str = None):
        """
        This method sends an embedded discord message when a !run command is invoked
        containing the information about the requested run

        :param ctx: represents the context in which a command is being invoked under
        (https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#context)
        :param run_id: the link to the run
        :param season: name of the season to retrieve (season-df-1, etc.). Defaults to current season.

        """
        run_id = (run_id.split("-")[4]).split("/")[1]
        if season is None:
            data = self.parser.ParseMythicRun('season-df-2', run_id)
        else:
            data = self.parser.ParseMythicRun(season, run_id)
        time = str(
            (int(data['clear_time_ms']) // 60000)) + ":" + str(
            int((int(data['clear_time_ms']) % 60000) / 1000))
        if data['time_remaining_ms'] > 0:
            descr = "yes"
        else:
            descr = "no"
        embedded_message = discord.Embed(title=data['dungeon']['name'], color=0x394A8C)
        embedded_message.add_field(name="Keystone level:", value=data['mythic_level'], inline=False)
        embedded_message.add_field(name="Time of completion:", value=time, inline=False)

        roster_info = ""
        for member in data['roster']:
            character = member['character']
            spec = character['spec']
            item_level = member['items']['item_level_equipped']

            roster_info += f"{character['name']} - {spec['name']} {character['class']['name']} ({spec['role']})\n"
            roster_info += f"**item level:** {item_level}\n"

        embedded_message.add_field(name="Members:", value=roster_info, inline=False)
        embedded_message.add_field(name="Deaths:", value=len(data['logged_details']['deaths']))
        embedded_message.add_field(name="Keystone timed:", value=descr)

        picture = "https://cdnassets.raider.io" + data['dungeon']['icon_url']
        embedded_message.set_thumbnail(url=picture)
        await ctx.send(embed=embedded_message)
