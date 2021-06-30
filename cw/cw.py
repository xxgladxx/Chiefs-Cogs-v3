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
        embed1 = discord.Embed()
        numberoffields = 0
        await ctx.send("```py\n'Please wait upto 2-4 minutes..'```")
        for member in participants:
            if self.checkmember(tag = member["tag"]) == True:
                if numberoffields <= 25:
                    embed.add_field(name=f"```{member['name']} - {member['tag']}```", value = f"```{member['decksUsedToday']}```")
                    numberoffields = numberoffields + 1
                else:
                    embed1.add_field(name=f"```{member['name']} - {member['tag']}```", value = f"```{member['decksUsedToday']}```")
                    

        await ctx.send(embed = embed)
        await ctx.send(embed = embed1)

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
            
