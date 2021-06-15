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

#datetime
from datetime import datetime



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
    

    def cog_unload(self):
       if self.clash:
           self.bot.loop.create_task(self.clash.close())

    @commands.command()
    async def cls(self, ctx, member: discord.Member = None, account: int = 1):
        """Check last seen in Clash Royale"""
        if member is None:
            member = ctx.author
         
        user_tag = '#' + str(self.tags.getTag(member.id, account))
        player_data = await self.clash.get_player(user_tag)
        if player_data.clan is None:
            return await ctx.send(f"Sorry, {player_data.name} is not in a clan.\nHence, I could not track their last seen.") 
        else:
            clan_data = await self.clash.get_clan_members(player_data.clan.tag)

        
        async for data in clan_data:

            if str(data.tag) == user_tag:
                ls = data.lastSeen
                
        lastseen = datetime.strftime(datetime.strptime(ls, '%Y%m%dT%H%M%S.%fZ'), "%d/%m/%Y, %H:%M:%S")
        difference = datetime.strftime(datetime.now() - datetime.strptime(ls, '%Y%m%dT%H%M%S.%fZ'), "%d/%m/%Y, %H:%M:%S")
        
        await ctx.send("The user was last seen at:\n{} UTC, i-e,\n{} from now".format(lastseen, difference))
    
    
    
    
    
        
        #await ctx.send_interactive(pagify(data))
