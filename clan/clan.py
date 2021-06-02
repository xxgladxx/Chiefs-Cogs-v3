import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.embed import randomize_colour
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from random import choice
import clashroyale

class ClashRoyaleCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2512325)
        default_user = {"tag" : None, "nick" : None}
        self.config.register_user(**default_user)
        default_guild = {"clans" : {}}
        self.config.register_guild(**default_guild)
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        
    async def initialize(self):
        keys = await self.bot.get_shared_api_tokens("crapi")
        apikey = keys.get("api_key")
        if apikey is None:
            raise ValueError("The Clash Royale API key has not been set. Use [p]set api crapi api_key,YOURAPIKEY")
        self.crapi = clashroyale.OfficialAPI(apikey, is_async=True)
  
     
    async def chiefstry(self, ctx):
      clan = await self.crapi.get_clan('#YGGQR0CV')
      await ctx.send(clan)
