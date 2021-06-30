from .cw import ClanWarCog

async def setup(bot):
  cog = ClanWarCog(bot)
  bot.add_cog(cog)
