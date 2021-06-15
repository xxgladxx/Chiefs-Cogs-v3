from .clseen import ClashLastSeen

async def setup(bot):
    cog = ClashLastSeen(bot=bot)
    await cog.crtoken()
    bot.add_cog(cog)

        
