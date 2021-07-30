from .clanhistory import ClashRoyaleHistory

def setup(bot):
    bot.add_cog(ClashRoyaleHistory(bot=bot))