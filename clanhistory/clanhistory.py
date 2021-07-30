#importing modules
from redbot.core import commands, checks
import requests
from bs4 import BeautifulSoup
import discord

class ClashRoyaleHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
    
    async def formatter(self, text: str):
        self.new_data = ""
        pos = ""
        co = 'Co-Leader'
        el = 'Elder'
        le = 'Leader'
        me = 'Member'
        if co in text:
            text = text.replace(co , "-")
            pos = co
        elif el in text:
            text = text.replace(el, '-')
            pos = el
        elif le in text:
            text = text.replace(le, '-')
            pos = le
        elif me in text:
            text = text.replace(me, '-')
            pos = me
        date = text[:-10]
        text = text.replace(date, "")
        self.new_data = f'{text}\n{date}\n{pos}'

        
    @checks.admin()
    @commands.command(aliases = ['ch'])
    async def clanhistory(self, ctx, member: discord.Member = None, account: int = 1):
        if member is None:
            member = ctx.author
        try:
            profiletag = self.tags.getTag(member.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                      "Use !save <tag> to save a tag or that account number doesn't exist,"
                                      " use !accounts to see the accounts you have saved")
        except Exception as e:
            return await ctx.send(e) 
        profiletag = profiletag.strip('#')    
        url = f'https://clashratings.com/cr/player/{profiletag}'
        result = requests.get(url)
        data = result.content.decode('utf-8')
        soup = BeautifulSoup(data)
        #content = str(soup.prettify)
        divs = soup.find_all("div", {"class": "playerClanHistoryResults"})
        output = ""
        number = 1
        if divs is not None:
            for div in divs:
                await ctx.send(div.text)
                # await self.formatter(div.text)
                # output = f'{number}. {output}\n'
                # number = number + 1
                # await ctx.send(f'```\n{output}\n```')
        else:
            await ctx.send("Could not fetch the clan history of this user.")
