from redbot.core import commands
import discord

class WLCM(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        
  #  @commands.Cog.listener()
   # async def on_member_join(self, member : discord.Member) -> None:
        # send a message to welcome channel when a user joins server
    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member ):
        channel = member.guild.get_channel(827982101507866726)
        embed = discord.Embed(color=discord.Colour.green(), description=f"Welcome to Chiefs United! \n {user} \n\n _If your main purpose is to **Chill** and **Kill**, you are at the right place! _ \n\n ➼ Founded on 29th September 2020, we aim for the best clashing experience in a friendly environment. We provide you a wonderful place to hang around with other chiefs.  \n➼ If you have already joined our clan in-game, or wanna stay in this server as a <@&760377954726707200>, verify your CR account by typing the following command here :- \n!save <tag><api_token> \n\n ➼ If you wanna join our alliance, ping a <@&760377944043814942>.\n\n ➼ If you're facing any trouble, ping <@&760484038062112808> in this channel. \n\n Have Fun,\n Clash On! \n\n**⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢**")
        embed.set_author(name="⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢⇢", icon_url="https://media.discordapp.net/attachments/754780357349605467/760477780978434058/image0.gif?width=475&height=475", url="https://discord.gg/WNrSEGVT")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/wtqLXQjEmYQLdwmAUUo0gMMutN6MApAxnfHSqsMds7c/%3Fwidth%3D473%26height%3D473/https/media.discordapp.net/attachments/827982101507866726/829589928807497768/legend_logo-trans.png")
        embed.set_image(url="https://cdn.discordapp.com/emojis/576516555714592796.gif?v=1")
        embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
        await channel.send(embed=embed,allowed_mentions=discord.AllowedMentions(roles=True))
        await member.send('https://link.clashroyale.com/en?clanInfo?id=YGGQR0CV')
