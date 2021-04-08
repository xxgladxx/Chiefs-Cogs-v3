from redbot.core import commands
import discord

class WLCM(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        
  #  @commands.Cog.listener()
   # async def on_member_join(self, member : discord.Member) -> None:
        # send a message to welcome channel when a user joins server
    @commands.command()
    async def wlcm(self, ctx):
        channel = ctx.guild.get_channel(827982101507866726)
        await channel.send('Hey')
