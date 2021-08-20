from .clashutils import ClashUtils

def setup(bot):
    cog = ClashUtils(bot)
    bot.add_cog(cog)
    