import discord
from redbot.core import commands
import clashroyale
import json
import urllib.request

class ClanWarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cwcheck(self, ctx):
        self.con = "No"
        token = await self.bot.get_shared_api_tokens("crapi")
        self.token = token["api_key"]
        complete_url = "https://api.clashroyale.com/v1/clans/%23YGGQR0CV/currentriverrace"
        req = urllib.request.Request(complete_url,
                                    None,
                                    {
                                        "Authorization": "Bearer %s" % self.token
                                    }
                                    )
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        clan_data = response['clan']
        participants = clan_data['participants']

        for member in participants:
            await self.checkmember(member["tag"])
            if self.con =='Yes':
                await ctx.send(f"{member['name']} - {member['tag']} - {member['decksUsedToday']}")

            
            

    async def checkmember(self, tag: str):
        url = "https://api.clashroyale.com/v1/clans/%23YGGQR0CV/members"
        req = urllib.request.Request(url,
                                    None,
                                    {
                                        "Authorization": "Bearer %s" % self.token
                                    }
                                    )
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        for member in response['items']:
            member_tag = member['tag']
            if member_tag == tag:
                self.con = "Yes"
            