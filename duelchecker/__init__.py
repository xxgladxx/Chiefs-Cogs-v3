from .duelchecker import DuelChecker

def setup(bot):
    cog = DuelChecker(bot=bot)
    bot.add_cog(cog)
    