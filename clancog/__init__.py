from .clancog import ClanCog
async def setup(bot):
    cog = ClanCog(bot=bot)
    await cog.token_init()
    bot.add_cog(cog)