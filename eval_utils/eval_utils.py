import discord
from redbot.core import commands

class EvalUtility(commands.Cog):

        def __init__(self, bot):
            self.bot = bot
            self.embed = discord.Embed()
        
        async def formatter(self, message):
            message = message[5:]
            message = message.strip("```").strip('py')
            self.embed.add_field(name="\u200b", value=f"```py\n{message}\n```")
            return self.embed
            



        @commands.Cog.listener()
        async def on_message(self, message = discord.Message):
            if message.author.id == 698376874186768384:
                if message.content.startsWith('!eval'):
                    await self.formatter(str(message.content))
                    await message.channel.send(self.embed)

