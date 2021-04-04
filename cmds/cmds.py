# Discord
import discord
import random

# Red
from redbot.core import commands

# Libs 
from random import choice as rnd

BaseCog = getattr(commands, "Cog", object)

__version__ = "2018.9.0"
__author__ = "Yukirin"

gifs = [
    "https://i.imgur.com/YTGnx49.gif",
    "https://i.imgur.com/U37wHs9.gif",
    "https://i.imgur.com/BU2IQym.gif",
    "https://i.imgur.com/yp6kqPI.gif",
    "https://i.imgur.com/uDyehIe.gif",
    "https://i.imgur.com/vG8Vuqp.gif",
    "https://i.imgur.com/z4uCLUt.gif",
    "https://i.imgur.com/ZIRC9f0.gif",
    "https://i.imgur.com/s8m4srp.gif",
    "https://i.imgur.com/LKvNxmo.gif",
    "https://i.imgur.com/j4W4GFt.gif",
    "https://i.imgur.com/75bX4A1.gif",
    "https://i.imgur.com/dSlfpe3.gif",
    "https://i.imgur.com/JjxaT8e.gif",
    "https://i.imgur.com/QWBlOaQ.gif",
    "https://i.imgur.com/5448px6.gif",
    "https://i.imgur.com/4WJRAGw.gif",
    "https://i.imgur.com/v1sSh5r.gif"
]

failmsgs = [
    "{author} is trying to pat non-existent entity ... and failed.",
    "{author}: *pats non-existent entity*. This bad boy can accept so many pats.",
    "To be honest, I don't know what's {author} been smoking, but sorry, you can't pat non-existent entity",
    "Oh come on, is it that hard to correctly use this command?",
    "You must pat valid and existing user. Try using @ mention, username or nickname.",
    "(╯°□°）╯︵ ┻━┻"
]

patmsgs = [
    "**{user}** got a pat from **{author}**",
    "**{author}** affectionately pat **{user}**",
    "Without hesitation, **{author}** pats **{user}** with love"
]


class PDA(BaseCog):
    """Public Display of Affection ~!"""

    def __init__(self, bot):
        self.gifs = gifs
        self.failmsgs = failmsgs
        self.version = __version__
        self.author = __author__

    @commands.command()
    @commands.cooldown(6, 60, commands.BucketType.user)
    async def pat(self, ctx, *, user: discord.Member=None):
        """Pat users."""
        author = ctx.author

        if not user:
            message = rnd(self.failmsgs)
            await ctx.send(message.format(author=author.name))
        else:
            message = rnd(patmsgs)
            pat = discord.Embed(description=message.format(user=user.name, author=author.name), color=discord.Color(0xffb6c1))
            pat.set_image(url=rnd(self.gifs))
            await ctx.send(embed=pat)

    @commands.command(name="pdaver", hidden=True)
    async def _pda_version(self, ctx):
        """Show PDA version"""
        ver = self.version
        await ctx.send("You are using PDA version {}".format(ver))
        
    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        """Hug your senpai/waifu!"""
        author = ctx.author.mention
        mention = member.mention
        
        hug = "**{0} gave {1} a hug!**"
        
        choices = ['http://i.imgur.com/sW3RvRN.gif', 'http://i.imgur.com/gdE2w1x.gif', 'http://i.imgur.com/zpbtWVE.gif', 'http://i.imgur.com/ZQivdm1.gif', 'http://i.imgur.com/MWZUMNX.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour.blue())
        embed.set_image(url=image)

        await ctx.send(embed=embed)

    @commands.command()
    async def mongoop(self, ctx):
        """Hug your senpai/waifu!"""
        
        embed = discord.Embed(colour=discord.Colour.blue(), description="No doubt!")
        embed.set_author(name="Yeeet!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/823464413910532109/828225135575302154/image0-removebg-preview.png")

        await ctx.send(embed=embed)
                        
    @commands.command()
    async def yerzop(self, ctx):
        """Hug your senpai/waifu!"""
        
        embed = discord.Embed(colour=discord.Colour.red(), description="No doubt!")
        embed.set_author(name="Wuhuuuu!")
        embed.set_image(url="https://media.discordapp.net/attachments/823464413910532109/828225199613804584/image0-removebg-preview_1.png")

        await ctx.send(embed=embed)

    @commands.command()
    async def daanop(self, ctx):
        """Hug your senpai/waifu!"""
        
        embed = discord.Embed(colour=discord.Colour.red(), description="Shhh:shushing_face:")
        embed.set_author(name="Mr.077!")
        embed.set_image(url="https://media.discordapp.net/attachments/823464413910532109/828230236122120192/821639162611630111.png")

        await ctx.send(embed=embed)
