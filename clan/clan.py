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
        
    @tasks.loop(seconds = 120)
    async def myLoop(self, ctx):
        await ctx.send("Loop test.")

  

    @commands.command()
    async def chiefstry(self, ctx):
      clan = str(await(self.crapi.get_clan('#YGGQR0CV')))
      await ctx.send_interactive(pagify((clan)))

    @commands.command(aliases=["z"])
    async def dev_z(self, ctx):
        self.myLoop.start()
