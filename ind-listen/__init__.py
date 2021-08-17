from .indlisten import IndListen

def setup(bot):
  bot.add_cog(IndListen(bot=bot))
