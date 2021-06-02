from .clan import ClashRoyaleCog

async def setup(self, bot):
  cog = ClashRoyaleCog(bot)
  await cog.initialize()
  bot.add_cog(cog)
