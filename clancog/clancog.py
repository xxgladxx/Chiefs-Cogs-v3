from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import pagify
import discord
import clashroyale
import urllib.request
import json

class ClanCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=82998018)
        member = {"tag" : None, "name" : None, "donations" : None, "cwfame" : None}
        self.config.register_user(**member)
    
    async def token_init(self):
        tokens = await self.bot.get_shared_api_tokens('crapi')
        self.token = tokens['api_key']
    
    @checks.is_owner()
    @commands.command(name = 'cwt')
    async def _cwt(self, ctx, clan: str):
        if clan is None:
            return await ctx.send("Please enter clan name\n`united` or `rising`")
        else:
            if clan.lower() == 'rising':
             tag = 'QY0JVUYG'
            elif clan.lower() == 'united':
             tag = 'YGGQR0CV'
            else:
             return await ctx.send("Please use the command with either `united` or `rising`")
        
        war_url = f"https://api.clashroyale.com/v1/clans/%23{tag.strip('#')}/currentriverrace"
        war_req = urllib.request.Request(war_url, None, {"Authorization": "Bearer %s" % self.token})
        war_data = json.loads((urllib.request.urlopen(war_req)).read().decode('utf-8'))
        #await ctx.send_interactive(pagify(war_data))
        #for item in war_data.keys():
        #    await ctx.send(item)
        for data in war_data['clans']:
           await ctx.send(type(data))
