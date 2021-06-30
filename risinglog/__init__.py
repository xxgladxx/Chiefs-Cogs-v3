from .risinglog import RisingLog

async def setup(bot):
  cog = RisingLog(bot)
  await cog.initialize()
  bot.add_cog(cog)
