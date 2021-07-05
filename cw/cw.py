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
                    embed.add_field(name=f"```{member['name']} - {member['tag']}```", value = f"```{member['decksUsedToday']}```", inline = True)
                    numberoffields = numberoffields + 1
                else:
                    embed1.add_field(name=f"```{member['name']} - {member['tag']}```", value = f"```{member['decksUsedToday']}```", inline = True)
                    

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
    
    @commands.command(name = 'cwchecker')
    async def _cwchecker(self, ctx, clan: str = None):
        tag = ''
        if clan is None:
            return await ctx.send("```py\n'\nClan name not mentioned.\nUse the command followed by clan name.\n'```")
        else:
            if clan.lower() == 'united':
                tag = 'YGGQR0CV'
            elif clan.lower() == 'rising':
                tag = 'QY0JVUYG'
            else:
                return await ctx.send("```py\n'\nPlease use the command with either united or rising.\n'```")
        token = await self.bot.get_shared_api_tokens("crapi")
        token = token["api_key"]
        complete_url = f"https://api.clashroyale.com/v1/clans/%23{tag}/currentriverrace"
        url = f"https://api.clashroyale.com/v1/clans/%23{tag}/members"
        req_1 = urllib.request.Request(url, None, {"Authorization": "Bearer %s" % token})
        rep = json.loads(urllib.request.urlopen(req_1).read().decode("utf-8"))

        req = urllib.request.Request(complete_url, None, {"Authorization": "Bearer %s" % token})
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

        today_0 = ""
        today_0_1 = ""
        today_u4 = ""
        today_u4_1 = ""
        yes_0 = ""
        yes_0_1 = ""
        yes_u4 = ""
        yes_u4_1 = ""
        decks_used = 0
        decks_used_today = 0

        clan_data = response['clan']
        participants = clan_data['participants']
        for member in participants:
         if member["tag"] in str(rep):
             if member['decksUsed'] == 0:
                 yes_0 = yes_0 + '\n' + member['name']  
             else:
                decks_used = member['decksUsed']
                decks_used_today = member['decksUsedToday']
             if decks_used_today == 0:
                today_0 = today_0 + "\n" + member['name']
                if decks_used < 4:
                    yes_u4 = yes_u4 + '\n' + member['name']

             if decks_used_today < 4 and decks_used_today > 0:
                    today_u4 = today_u4 + "\n" + member['name']

        await ctx.send(f"```py\n@Zero battles in both days:\n'{yes_0}\n'```")
        await ctx.send(f"```py\n@Under 4 battles yesterday:\n'{yes_u4}\n'```")
        await ctx.send(f"```py\n@Zero battles today:\n'{today_0}\n'```")
        await ctx.send(f"```py\n@Under 4 battles today:\n'{today_u4}\n'```")

    @commands.command(name='cwarner')
    async def _cwarner(self, ctx):
        complete_url = f"https://api.clashroyale.com/v1/clans/%23YGGQR0CV/currentriverrace"
        url = f"https://api.clashroyale.com/v1/clans/%23YGGQR0CV/members"
        req_1 = urllib.request.Request(url, None, {"Authorization": "Bearer %s" % self.token})
        rep = json.loads(urllib.request.urlopen(req_1).read().decode("utf-8"))

        req = urllib.request.Request(complete_url, None, {"Authorization": "Bearer %s" % self.token})
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        clan_data = response['clan']
        participants = clan_data['participants']
        count = 3
       
        for member in participants:
         if member["tag"] in str(rep):
             if count <= member['decksUsedToday']:
                for person in ctx.guild.members:
                  if person.name == f'{member["name"]} | United':
                    await ctx.send(f"Hey {person.mention}, you have {4-int(member['decksUsedToday'])} decks remaining for today. Please complete them ASAP or let a co-leader know if you can't.\nStay safe, chief!")
