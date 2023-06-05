# Toxicity - "bringing toxic back to wow"


### Elevator pitch
Have you always wanted to flex your DPS numbers to your friends? Had the desire to scream at your healers for not doing enough HPS (because surely your death is their fault)? 
Well, thanks to Toxicity now you can! Visualize the data of your latest wow raid and send it straight into your raid channel. Assert your dominance!
(warning, this bot is for god-gamers only)

### Project description
The main goal of the project is to create a discord bot, which will compare the individual and group performance in the MMORPG World of Warcraft. The bot will pull data from the raider.io API (https://raider.io/) and the Warcraft Logs API (https://www.warcraftlogs.com/) and will process it and give out statistics about the requested performance.

### UML diagram description
On the UML diagram (see Toxicity.drawio.png) we have class Toxicity Bot which will initialize the bot and connect it with the desired server channel.
Going down, we have an abstract class ApiClient that has a Request() method which will be the basis of how requests work in both of the APIs. 
WCLApiConnector and RaiderIOApiConnector inherit from it, but both APIs work differently. Even though the diagram looks symmetrical, **the symmetry breaks because of the output of the methods**.

#### Warcraft Logs API classes
Let's focus on the Warcraft Logs API classes for now. We have the Connector class which requires client ID and a secret key acquired from the warcraft logs website. The API technology used here is OAuth 2.0, that's why we must create the OAuth session and also take care of the expiry date of the token. We can only send one request to the API at a time. Then moving on we have a WCLParser class that will parse the JSON file given to us by the API and change it to a Pandas library DataFrame structure. Then finally in a WCLCog (which inherits discord.cog) it will transform the data given into either a graph or a simple discord message when a command will be written in the discord channel.

#### RaiderIO API Classes
This API on the other hand does not require any identification of the user, we can send multiple request directly to the API (see more at https://raider.io/api). The data we get from the API will be in a JSON form, which we will then convert into a Pandas DataFrame in the RaiderIOParser. In the RaiderIOCog (which inherits discord.cog) we convert the DataFrame further into a graph or a message.
