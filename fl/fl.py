import discord
from redbot.core import commands
import asyncio

class FL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_without_command(self, message):

        user=message.author
        if "https://link.clashroyale.com/invite/friend" in message.content:
            embed = discord.Embed(color=user.colour, description=user.mention)
            embed.set_author(name="Chiefs United!", icon_url=user.avatar_url)
            embed.set_thumbnail(url="https://media.tenor.co/videos/89c5ae3cdef45e20658074f4d3e386e0/mp4")
            embed.add_field(name="Click the link below to add "+str(user.name)+" in Clash Royale!", value="\u200B")
            embed.add_field(name="Link", value=f"[click]({message.content})")
            embed.set_footer(text="Bot by Gladiator#0004", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
            await message.channel.send(embed=embed)
            await message.delete()
