import discord
import ToxicityBot

bot_token = None


class Main:
    # initialize the bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = ToxicityBot.ToxicityBot(intents=intents, command_prefix='!')
    client.run(bot_token)


