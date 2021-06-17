from datetime import datetime
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

class Emojis(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def emoji(self, ctx, emoji_name: str):
        """Returns all the inbuild bot emojis that contain the word given by the user."""
        if emoji_name is None:
             return await ctx.send("No emoji name given")                 
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                if emoji_name in emoji.name.lower():
                    name = emoji.name + (".gif" if emoji.animated else ".png")
                    url = str(emoji.url).replace("<Asset url='", "")
                    url = url.replace("'>", "")
                    embed=discord.Embed(color=discord.Colour.green())
                    embed.set_image(url=url)
                    await ctx.send(embed=embed)
                    
 
  @commands.command()
  async def listemojis(self, ctx):
    """lists emojis that bot has"""
    embed = discord.Embed()
    out=[]
    for guild in self.bot.guilds:
              for emoji in guild.emojis:
                name = emoji.name
                out.append(f":{name}:")
    pages = []
    for page in pagify("\n".join(out), shorten_by=24):
            embed = discord.Embed(description=page, timestamp=datetime.utcnow(),)
            embed.set_footer(text="By Nubiator6969", icon_url=ctx.author.avatar_url)
            pages.append(embed)
    await menu(ctx, pages, DEFAULT_CONTROLS, timeout=120)
      

                 


