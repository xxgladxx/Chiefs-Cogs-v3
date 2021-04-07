from redbot.core import commands
import discord

class AutoRole(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        """ADD AUTOROLE"""
        # Your code will go here
        role = discord.utils.get(member.server.roles, id="821778143937167372")
        await self.bot.add_roles(member, role)
