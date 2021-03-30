import discord
import re
import urllib.parse as urlparse
import clashroyale
from redbot.core import commands

creditIcon = "https://i.imgur.com/TP8GXZb.png"
credits = "Bot by GR8 | Titan"


class friendlink(commands.Cog):
    """Automatically convert Clash Royale and Brawl Stars friend links to beautiful embeds"""

    def __init__(self, bot):
        self.bot = bot
        self.CRregex = re.compile(r"<?(https?:\/\/)?(www\.)?(link\.clashroyale\.com\/invite\/friend)\b([-a-zA-Z0-9/]*)>?")
        self.auth = self.bot.get_cog('cr').auth
        self.tags = self.bot.get_cog('cr').tags
        self.constants = self.bot.get_cog('cr').constants
        self.clash = clashroyale.OfficialAPI(self.auth.getOfficialToken(), is_async=True)

    def emoji(self, name):
        """Emoji by name."""
        for emoji in self.bot.get_all_emojis():
            if emoji.name == name:
                return '<:{}:{}>'.format(emoji.name, emoji.id)
        return ''

    def getLeagueEmoji(self, trophies):
        """Get BS League Emoji"""
        mapLeagues = {
            "starLeague": [10000, 90000],
            "masterLeague": [8000, 9999],
            "crystalLeague": [6000, 7999],
            "diamondLeague": [4000, 5999],
            "goldLeague": [3000, 3999],
            "silverLeague": [2000, 2999],
            "bronzeLeague": [1000, 1999],
            "woodLeague": [0, 999]
        }
        for league in mapLeagues.keys():
            if mapLeagues[league][0] <= trophies <= mapLeagues[league][1]:
                return self.emoji(league)

    @commands.Cog.listener()
    async def friend_link_cr(self, message):

        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)

        try:

            parsed = urlparse.urlparse(url[0])
            profiletag = urlparse.parse_qs(parsed.query)['tag'][0]

            try:
                profiledata = await self.clash.get_player(profiletag)
            except clashroyale.RequestError:
                return

            arenaFormat = profiledata.arena.name.replace(' ', '').lower()

            embed = discord.Embed(title='Click this link to add as friend in Clash Royale!', url=url[0], color=0x0080ff)
            embed.set_author(name=profiledata.name + " (" + profiledata.tag + ")", icon_url=await self.constants.get_clan_image(profiledata))
            embed.set_thumbnail(url="https://imgur.com/C9rLoeh.jpg")
            embed.add_field(name="User", value=message.author.mention, inline=True)
            embed.add_field(name="Trophies", value="{} {:,}".format(self.emoji(arenaFormat), profiledata.trophies), inline=True)
            embed.add_field(name="Level", value=self.emoji("level{}".format(profiledata.expLevel)), inline=True)
            if profiledata.clan is not None:
                embed.add_field(name="Clan {}".format(profiledata.role.capitalize()),
                                value="{} {}".format(self.emoji("clan"), profiledata.clan.name),
                                inline=True)
            embed.set_footer(text=credits, icon_url=creditIcon)

            await self.bot.send_message(message.channel, embed=embed)
            await self.bot.delete_message(message)

        except Exception as e:
            return

    async def on_message(self, message):

        author = message.author

        if author.id == self.bot.user.id:
            return

        if self.CRregex.search(message.content) is not None:
            return await self.friend_link_cr(message)
