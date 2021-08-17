from redbot.core import commands
import discord

class IndListen(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
   
  @commands.Cog.listener()
  async def on_member_join(ctx, member):
   channel = ctx.guild.get_channel(876900213938356247)
   embed = discord.Embed(color = int('FFA500', 16),description=f'Welcome to {ctx.guild.name}, {member.mention}!\nPlease abide by the rules listed in <#877061646126809148> and set yourself up through <#877056352441229322>.\nThank you:)')
   await channel.send(content = f'{member.mention}', embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
