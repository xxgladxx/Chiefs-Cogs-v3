from .clseen import ClashLastSeen

async def setup(bot):
    cog = ClashLastSeen()
    await bot.crtoken
    bot.add_cog(cog)

        
