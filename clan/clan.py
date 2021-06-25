#
import discord
from redbot.core import Config, checks, commands
from discord.ext import tasks
from redbot.core.utils.chat_formatting import pagify
import clashroyale
import datetime
import asyncio

class ClashRoyaleCog(commands.Cog):
    """Checks clan log by using old collected data vs the refreshed data from crapi"""
    
    def __init__(self, bot):
        self.bot = bot
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        
    async def initialize(self):
        keys = await self.bot.get_shared_api_tokens("crapi")
        apikey = keys.get("api_key")
        if apikey is None:
            raise ValueError("The Clash Royale API key has not been set. Use [p]set api crapi api_key,YOURAPIKEY")
        self.clash = clashroyale.OfficialAPI(apikey, is_async=True)
        
    @tasks.loop(seconds = 20)
    async def checker(self, ctx):
        await self.nclan_data()
        time = datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        x = 0
        if self.clan_type != self.nclan_type:
            await ctx.send(f"```py\n'The clan type was changed from {self.clan_type} to {self.nclan_type} at {time} UTC'```")
            self.clan_type = self.nclan_type
        if self.old_req != self.new_req:
            await ctx.send(f"```py\n'The required trophies were changed from {self.old_req} to {self.new_req} at {time} UTC'```")
            self.old_req = self.new_req
        if self.clan_desc != self.nclan_desc:
            await ctx.send(f"The clan description was changed from\n```py\n'{self.clan_desc}'```\nto\n```py\n'{self.nclan_desc}'```\nat {time} UTC")
            self.clan_desc = self.nclan_desc
        #TODO : Add self.clan_logo_id and it's updated id.
        if self.clan_cwtrophy != self.nclan_cwtrophy:
            await ctx.send(f"Clan war trophies updated.\n```py\n'From: {self.clan_cwtrophy} to {self.nclan_cwtrophy} at {time}'```")
            self.clan_cwtrophy = self.nclan_cwtrophy
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
        self.old_clan_data = await self.clash.get_clan('#YGGQR0CV')
        self.old_clan_members = await self.clash.get_clan_members('#YGGQR0CV')
        self.clan_type = str(self.old_clan_data.type)
        self.clan_desc = str(self.old_clan_data.description)
        self.clan_logo_id = str(self.old_clan_data.badgeId)
        self.clan_cwtrophy = str(self.old_clan_data.clanWarTrophies)
        self.members = str(self.old_clan_data.members)
        self.old_req = str(self.old_clan_data.requiredTrophies)
    
    async def nclan_data(self):
        """fetches refreshed clanlog"""
        self.new_clan_data = await self.clash.get_clan('#YGGQR0CV')
        self.new_clan_members = await self.clash.get_clan_members('#YGGQR0CV')
        self.nclan_type = str(self.new_clan_data.type)
        self.nclan_desc = str(self.new_clan_data.description)
        self.nclan_logo_id = str(self.new_clan_data.badgeId)
        self.nclan_cwtrophy = str(self.new_clan_data.clanWarTrophies)
        self.nmembers = str(self.new_clan_data.members)
        self.new_req = str(self.new_clan_data.requiredTrophies)


    async def chiefstry(self, ctx):
      clan = str(await(self.crapi.get_clan('#YGGQR0CV')))
      await ctx.send_interactive(pagify((clan)))

    @commands.command(aliases=["z"])
    async def startclanlog(self, ctx):
        """Starts the clanlog"""
        await ctx.send("Started clan log.")
        await self.oclan_data()
        await self.checker.start(ctx)



    @commands.command()
    async def stopclanlog(self, ctx):
        """Stops the clanlog""" 

        var = self.checker.cancel()
        if var is None:
            await ctx.send("Clan log stopped successfully")
        else:
            await ctx.send("There was an issue stopping the clan log.\nPlease contact the bot dev.")
            

    @commands.command()
    async def refreshclanlog(self, ctx):
        """used to restart the clan log\nincase of maintenance break or some other cr api issues"""
        await ctx.send("Stopping clan log")
        await asyncio.sleep(10) 
        try:
          self.checker.cancel()
        except Exception as e:
          return await ctx.send(f"```py\n{e}```")
        await ctx.send("Refreshing clan log")
        await asyncio.sleep(10)
        try:
          await self.oclan_data()
          await self.checker.start(ctx)
        except Exception as e:
          return await ctx.send(f"```py\n{e}```")
        await ctx.send("Refreshed successfully!")


    @checks.is_owner()
    @commands.command()
    async def crapidata(self, ctx):
        data = str(clashroyale)
        await ctx.send(dir(clashroyale))


