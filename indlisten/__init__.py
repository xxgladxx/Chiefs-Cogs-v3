from .indlisten import IndListen

def setup(bot):
  cog = IndListen(bot=bot)
  bot.add_cog(cog)
