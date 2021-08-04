import discord
from redbot.core import commands, checks

class ListenToEval(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cleanup = self.bot.get_cog('Dev')
        for guild in bot.guilds:
            if guild.id == 760377603982360597:
                self.channel = guild.get_channel(860086183362822144)

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def evalreaction(self, payload):
     if payload.member.id == 698376874186768384 or 482470393333022720:
      if 'printer' in payload.emoji.name.strip(':').lower(): 
        for guild in self.bot.guilds:
            if guild.id == payload.guild_id:
                cChannel = guild.get_channel(payload.channel_id)
                message = await cChannel.fetch_message(payload.message_id)
        message = self.cleanup.cleanup_code(message.content.strip('!eval'))
        file = open('code.py', 'w+')
        file.write(self.cleanup.cleanup_code(message))
        await self.channel.send(file=discord.File('code.py'))
