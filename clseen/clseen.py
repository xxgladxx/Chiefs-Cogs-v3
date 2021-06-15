#discord
import discord

#commands
from redbot.core  import commands

#clashroyale
import clashroyale

#asyncio
import asyncio



class ClashLastSeen(commands.Cog):
    """A CR related command"""

    def __init__(self, bot):
        # Certain initializations
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants

    async def crtoken(self):
        # Clash Royale API config
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Make sure to have royaleapi ip added (128.128.128.128) Use !set api clashroyale token,YOUR_TOKEN to set it")
        self.clash = clashroyale.official_api.Client(token=token['token'], is_async=True, url="https://proxy.royaleapi.dev/v1")
    

    

    @commands.command()
    async def cls(self, ctx, member = discord.Member):
        """Check last seen in Clash Royale"""
        if member is None:
            member = ctx.author
        
        data = self.clash.get_clan_war_log("#YGGQR0CV")
        await ctx.send(data)
