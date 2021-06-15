#discord
import discord

#commands
from redbot.core  import commands

#clashroyale
import clashroyale

#asyncio
import asyncio

#pagify
from redbot.core.utils.chat_formatting import pagify



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
    async def cls(self, ctx, member = discord.Member, account: int = 1):
        """Check last seen in Clash Royale"""
        if member is None:
            member = ctx.author
        
        clan_data = str(await self.clash.get_clan_members("#YGGQR0CV"))
        user_tag = str(self.tags.getTag(member.id, account))
        
        for data in clan_data:
            if data.tag == user_tag:
                await ctx.send(data.lastSeen)
        
        #await ctx.send_interactive(pagify(data))
