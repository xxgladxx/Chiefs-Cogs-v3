from .listentoeval import ListenToEval

def setup(bot):
    bot.add_cog(ListenToEval(bot=bot))
