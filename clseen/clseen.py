#discord
import discord
#commands
from redbot.core  import commands, checks
#clashroyale
import clashroyale
#datetime
from datetime import datetime

from redbot.core.utils.chat_formatting import pagify

class ClashLastSeen(commands.Cog):
    """A CR related command\nIncludes certain commands that are being build"""

    def __init__(self, bot):

        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants

    async def crtoken(self):

        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Make sure to have royaleapi ip added (128.128.128.128) Use !set api clashroyale token,YOUR_TOKEN to set it")
        self.clash = clashroyale.official_api.Client(token=token['token'], is_async=True, url="https://proxy.royaleapi.dev/v1")
   
    def cog_unload(self):
        if self.token_task:
            self.token_task.cancel()
        if self.clash:
            self.bot.loop.create_task(self.clash.close()) 


    @commands.command(aliases = ["cls"])
    async def clashlastseen(self, ctx, member: discord.Member = None, account: int = 1):
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
        format = "%d/%m/%Y, %H:%M:%S"        
        difference = str(datetime.utcnow() - datetime.strptime(ls, '%Y%m%dT%H%M%S.%fZ'))
        index = difference.rindex(':')
        difference = difference[:index].replace(':','h ') + 'm'
        embed = discord.Embed(description = f"The user was last seen at\n{difference} from now")
        embed.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        await ctx.send(embed=embed)
        
        
    @checks.is_owner()       
    @commands.command(aliases = ["clseen"])
    async def clashlastseentest(self, ctx, member: discord.Member = None, account: int = 1):
        """Check last seen in Clash Royale\nData Test"""
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
        format = "%d/%m/%Y, %H:%M:%S"        
        difference = str(datetime.utcnow() - datetime.strptime(ls, '%Y%m%dT%H%M%S.%fZ'))
        await ctx.send(datetime.strptime(ls, '%Y%m%dT%H%M%S.%fZ'))
        #index = difference.rindex(':')
        #difference = difference[:index].replace(':','h ') + 'm'
        #embed = discord.Embed(description = f"The user was last seen at\n{difference} from now")
        #embed.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
        #await ctx.send(embed=embed)        
       
    @checks.is_owner()       
    @commands.command(aliases = ["chief"])
    async def chiefclan(self, ctx):
        """A command under build"""
        clan_data = await self.clash.get_clan_war_log('#YGGQR0CV')
        await ctx.send_interactive(pagify(clan_data))

