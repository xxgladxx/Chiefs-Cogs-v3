import discord
from redbot.core import Config, checks, commands
from discord.ext import tasks
from redbot.core.utils.chat_formatting import pagify
import clashroyale
from datetime import datetime

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
        
    @tasks.loop(seconds = 120)
    async def checker(self, ctx):
        await self.nclan_data()
        if self.clan_type != self.nclan_type:
            await ctx.send(f"```py\nThe clan type was changed from {self.clan_type} to {self.nclan_type} at {datetime.utcnow} UTC")
            self.clan_type = self.nclan_type

        if self.clan_desc != self.nclan_desc:
            await ctx.send(f"The clan description was changed from\n```py\n{self.clan_desc}```\nto\n```py\n{self.nclan_desc}```\nat {datetime.utcnow} UTC")
            self.clan_desc = self.nclan_desc
        #if self.clan_logo_id != self.nclan_logo_id:
        #will add this later
        if self.clan_cwtrophy != self.nclan_cwtrophy:
            await ctx.send(f"Clan war trophies updated.\n```py\nFrom: {self.clan_cwtrophy} to {self.nclan_cwtrophy} at {datetime.utcnow}```")
            self.clan_cwtrophy = self.nclan_cwtrophy
        # self.members != self.nmembers:
            #if int(self.members, 10) > int(self.nmembers, 10):
                #for data in self.old_clan_data:
                    #for ndata in self.new_clan_data()        
        
        


    async def oclan_data(self):
        """The clan data code goes here"""
        self.old_clan_data = await self.clash.get_clan('#YGGQR0CV')
        self.clan_type = str(self.old_clan_data.type)
        self.clan_desc = str(self.old_clan_data.description)
        self.clan_logo_id = str(self.old_clan_data.badgeId)
        self.clan_cwtrophy = str(self.old_clan_data.clanWarTrophies)
        self.members = str(self.old_clan_data.members)
    
    async def nclan_data(self):
        self.new_clan_data = await self.clash.get_clan('#YGGQR0CV')
        self.nclan_type = str(self.new_clan_data.type)
        self.nclan_desc = str(self.new_clan_data.description)
        self.nclan_logo_id = str(self.new_clan_data.badgeId)
        self.nclan_cwtrophy = str(self.new_clan_data.clanWarTrophies)
        self.nmembers = str(self.new_clan_data.members)



    #@commands.command()
    async def chiefstry(self, ctx):
      clan = str(await(self.crapi.get_clan('#YGGQR0CV')))
      await ctx.send_interactive(pagify((clan)))

    @commands.command(aliases=["z"])
    async def startclanlog(self, ctx):
        """Starts the clanlog"""
        await ctx.send("Started clan log.")
        await self.old_clan_data()
        await self.checker.start(ctx)

    @commands.command()
    async def stopclanlog(self, ctx):
        """Stops the clanlog""" 

        var = self.checker.cancel()
        if var is None:
            await ctx.send("Clan log stopped successfully")
        else:
            await ctx.send("There was an issue stopping the clan log.\nPlease contact the bot dev.")
