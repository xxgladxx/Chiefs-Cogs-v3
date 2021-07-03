#
import discord
from redbot.core import checks, commands
from discord.ext import tasks
import clashroyale
import datetime

class RisingLog(commands.Cog):
    """Checks clan log by using old collected data vs the refreshed data from crapi"""
    
    def __init__(self, bot):
        self.bot = bot
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        
    async def initialize(self):
        keys = await self.bot.get_shared_api_tokens("crapi")
        apikey = keys.get("api_key")
        self.clash = clashroyale.OfficialAPI(apikey, is_async=True)
        
    @tasks.loop(seconds = 20)
    async def checker(self, ctx):
        await self.nclan_data()
        time = datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        if self.members != self.nmembers:
            if int(self.members, 10) > int(self.nmembers, 10): #means if someone left the clan
                async for data in self.old_clan_members:
                    tag = str(data.tag)
                    if tag not in str(self.new_clan_members):   
                        await ctx.send(f"Clan member list updated\n{self.members} -> {self.nmembers}\n```py\n'{data.name} - {tag} left the clan.\nat {time}'```")
                        self.old_clan_members = self.new_clan_members
                        return

            elif int(self.members, 10) < int(self.nmembers, 10): #means if someone joined the clan
                async for data in self.new_clan_members:
                    tag = str(data.tag)
                    if tag not in str(self.old_clan_members):
                        await ctx.send(f"Clan member list updated\n{self.members} -> {self.nmembers}\n```py\n'{data.name} - {tag} joined the clan.\nat {time}'```")
                        self.old_clan_members = self.new_clan_members
                        return
                        
 

    async def oclan_data(self):
        """The old clan data code goes here"""
        self.old_clan_data = await self.clash.get_clan('#QY0JVUYG')
        self.old_clan_members = await self.clash.get_clan_members('#QY0JVUYG')
        self.members = str(self.old_clan_data.members)
    
    async def nclan_data(self):
        """fetches refreshed clanlog"""
        self.new_clan_data = await self.clash.get_clan('#QY0JVUYG')
        self.new_clan_members = await self.clash.get_clan_members('#QY0JVUYG')
        self.nmembers = str(self.new_clan_data.members)

    @checks.admin()
    @commands.command(name = "startrisinglog")
    async def _startclanlog(self, ctx):
        """Starts the clanlog"""
        await self.oclan_data()
        await self.checker.start(ctx)

    @checks.admin()
    @commands.command(name = "stoprisinglog")
    async def _stopclanlog(self, ctx):
        """Stops the clanlog""" 
        var = self.checker.cancel()
