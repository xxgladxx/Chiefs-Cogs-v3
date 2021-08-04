import discord
from redbot.core import commands, checks

class ListenToEval(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cleanup = self.bot.get_cog('Dev')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
     if user.id == 698376874186768384 or user.id == 482470393333022720:
      if 'printer' in reaction.emoji:
        msg = (reaction.message.content)
        file = open('code.py', 'w+')
        file.write(self.cleanup.cleanup_code(msg))
        for guild in self.bot.guilds:
          if guild.id == 760377603982360597:
            channel = guild.get_channel(860086183362822144)
            await channel.send(file=discord.File('code.py'))
