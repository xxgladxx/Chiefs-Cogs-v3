from .clseen import ClashLastSeen

async def setup(bot):
    cog = ClashLastSeen(bot)
    await bot.crtoken
    bot.add_cog(cog)

        
