import discord
from redbot.core import Config, checks, commands
from discord.ext import tasks
from redbot.core.utils.chat_formatting import pagify
import clashroyale

class ClashRoyaleCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        
    async def initialize(self):
        keys = await self.bot.get_shared_api_tokens("crapi")
        apikey = keys.get("api_key")
        if apikey is None:
            raise ValueError("The Clash Royale API key has not been set. Use [p]set api crapi api_key,YOURAPIKEY")
        self.crapi = clashroyale.OfficialAPI(apikey, is_async=True)
        
    @tasks.loop(seconds = 10)
    async def myLoop(self, ctx):
        channel = ctx.guild.get_channel(854566618633863198)
        await channel.send("Loop test.")

  

    @commands.command()
    async def chiefstry(self, ctx):
      clan = await self.crapi.get_clan('#YGGQR0CV')
      stringA = ""
      for data in str(clan):
            if 'memberList' in data:
                break
            else:
                stringA = stringA.replace(stringA, str(clan))
                
      await ctx.send(stringA)

    @commands.command(aliases=["z"])
    async def dev_z(self, ctx):
        await ctx.send("trying to start loop")
        await self.myLoop.start(ctx)

    @commands.command()
    async def stopclanlog(self, ctx):

        var = self.myLoop.cancel()
        if var is None:
            await ctx.send("Clan Log stopped successfully")
        else:
            await ctx.send("There was an issue stopping the clan log.\nPlease contact the bot dev.")
