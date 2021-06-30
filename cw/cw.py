import discord
from redbot.core import commands
import clashroyale
import json
import urllib.request

class ClanWarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cw")
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
        embed = discord.Embed(description = "Current race stats:")
        embed.set_author(name = "Chiefs United - #YGGQR0CV", icon_url=ctx.guild.icon_url)

        for member in participants:
            if self.checkmember(tag = member["tag"]):
                embed.add_field(name="\u200b", value = f"```{member['name']} - {member['tag']} - {member['decksUsedToday']}```")
        await ctx.send(embed = embed)

    def checkmember(self, tag):
        tag = str(tag)
        url = "https://api.clashroyale.com/v1/clans/%23YGGQR0CV/members"
        req = urllib.request.Request(url,
                                    None,
                                    {
                                        "Authorization": "Bearer %s" % self.token
                                    }
                                    )
        a_response = urllib.request.urlopen(req).read().decode("utf-8")
        if tag in str(a_response):
            return True
            
