from redbot.core import commands
import discord

class IndListen(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.list = [('lurk_panda', 'https://cdn.discordapp.com/emojis/821639153401462804.png'), ('PandaDracula', 'https://cdn.discordapp.com/emojis/821639156216234035.png'), ('PandaHeya', 'https://cdn.discordapp.com/emojis/821639157968404492.png'), ('PandaAdmireHat', 'https://cdn.discordapp.com/emojis/821639160594694166.png'), ('PandaAdmire', 'https://cdn.discordapp.com/emojis/821639160778457128.png'), ('PandaCool', 'https://cdn.discordapp.com/emojis/821639160879382528.png'), ('PandaDisgust', 'https://cdn.discordapp.com/emojis/821639161143885824.png'), ('PandaEr', 'https://cdn.discordapp.com/emojis/821639161353338890.png'), ('PandaHiyaBlind', 'https://cdn.discordapp.com/emojis/821639161365921802.png'), ('Pandauwu', 'https://cdn.discordapp.com/emojis/821639162486718495.png'), ('PandaUh', 'https://cdn.discordapp.com/emojis/821639162611630111.png'), ('PandaFish', 'https://cdn.discordapp.com/emojis/821639163380105299.png'), ('PandaCryn', 'https://cdn.discordapp.com/emojis/821639163484569610.png'), ('PandaAh', 'https://cdn.discordapp.com/emojis/821639163521531925.png'), ('PandaKing', 'https://cdn.discordapp.com/emojis/821639164034023424.png'), ('PandaSleep', 'https://cdn.discordapp.com/emojis/821639164394471444.png'), ('CuteDuckPanda', 'https://cdn.discordapp.com/emojis/821639164591996960.png'), ('PandaDuckCop', 'https://cdn.discordapp.com/emojis/821639164910764044.png'), ('PandaProfit', 'https://cdn.discordapp.com/emojis/821639166365270096.png'), ('PandaDevil', 'https://cdn.discordapp.com/emojis/821639166597136434.png'), ('PandaRee', 'https://cdn.discordapp.com/emojis/821639166659264542.png'), ('CryingPanda', 'https://cdn.discordapp.com/emojis/821639168349962270.png'), ('PandaHyper', 'https://cdn.discordapp.com/emojis/821639168714473472.png'), ('PandaSouless', 'https://cdn.discordapp.com/emojis/821639168844103710.png'), ('PandaHiyaPolice', 'https://cdn.discordapp.com/emojis/821639169142292501.png'), ('PandaHugg', 'https://cdn.discordapp.com/emojis/821639169200750603.png'), ('PandaPJay', 'https://cdn.discordapp.com/emojis/821639169218576424.png'), ('PandaSmart', 'https://cdn.discordapp.com/emojis/821639169297088562.png'), ('PandaPanky', 'https://cdn.discordapp.com/emojis/821639169658322974.png'), ('PandaTurnip', 'https://cdn.discordapp.com/emojis/821639169809448960.png'), ('pepesad', 'https://cdn.discordapp.com/emojis/821660188455993375.png'), ('sadcat', 'https://cdn.discordapp.com/emojis/821660188809363457.png'), ('giggle', 'https://cdn.discordapp.com/emojis/821660188897312769.png'), ('ily', 'https://cdn.discordapp.com/emojis/821660188909240321.png'), ('pepeheart', 'https://cdn.discordapp.com/emojis/821660188951052308.png'), ('sad', 'https://cdn.discordapp.com/emojis/821679836665479188.png'), ('cool', 'https://cdn.discordapp.com/emojis/821679836690644992.png'), ('farmer_grimace', 'https://cdn.discordapp.com/emojis/821679836787376139.png'), ('pensive', 'https://cdn.discordapp.com/emojis/821679837139042324.png'), ('no_sadness', 'https://cdn.discordapp.com/emojis/821679837168664586.png'), ('hot', 'https://cdn.discordapp.com/emojis/821679837269590016.png'), ('monkey_grimace', 'https://cdn.discordapp.com/emojis/821679837289644032.png'), ('7190_linkpepehype', 'https://cdn.discordapp.com/emojis/821680141088325662.png'), ('FeelsBanMan', 'https://cdn.discordapp.com/emojis/821680141230538772.png'), ('MonkaChrist', 'https://cdn.discordapp.com/emojis/821680141671202856.png'), ('monkaS', 'https://cdn.discordapp.com/emojis/821680141733330984.png'), ('monkaHmm', 'https://cdn.discordapp.com/emojis/821680141758365697.png'), ('festivepepe', 'https://cdn.discordapp.com/emojis/821680141864009742.png'), ('monkaStab', 'https://cdn.discordapp.com/emojis/821680142111080458.png'), ('MonkaWae', 'https://cdn.discordapp.com/emojis/821680142237564988.png')]
    self.animated = [('et', 'https://cdn.discordapp.com/emojis/821615474705039391.gif'), ('LOL', 'https://cdn.discordapp.com/emojis/821617795199664178.gif'), ('rblob', 'https://cdn.discordapp.com/emojis/821620905268215809.gif'), ('nonono', 'https://cdn.discordapp.com/emojis/821620906957733898.gif'), ('piglaugh', 'https://cdn.discordapp.com/emojis/821620907259854848.gif'), ('happyclap', 'https://cdn.discordapp.com/emojis/821620907922685962.gif'), ('arrow', 'https://cdn.discordapp.com/emojis/821620909227638804.gif'), ('emoji_1', 'https://cdn.discordapp.com/emojis/821620909806714922.gif'), ('sad', 'https://cdn.discordapp.com/emojis/821620911307751454.gif'), ('catdance', 'https://cdn.discordapp.com/emojis/821620911366733834.gif'), ('dance', 'https://cdn.discordapp.com/emojis/821620912172171284.gif'), ('pikahi', 'https://cdn.discordapp.com/emojis/821620914038112256.gif'), ('wow', 'https://cdn.discordapp.com/emojis/821654247035764746.gif'), ('yeet', 'https://cdn.discordapp.com/emojis/821658744445992970.gif'), ('fire', 'https://cdn.discordapp.com/emojis/821658745066487841.gif'), ('pepeshoot', 'https://cdn.discordapp.com/emojis/821658745226264616.gif'), ('pepeclap', 'https://cdn.discordapp.com/emojis/821658745880182814.gif'), ('grimface', 'https://cdn.discordapp.com/emojis/821658746655866900.gif'), ('guitar', 'https://cdn.discordapp.com/emojis/821658747285536778.gif'), ('pepehehe', 'https://cdn.discordapp.com/emojis/821658747318566942.gif'), ('owo', 'https://cdn.discordapp.com/emojis/821658747637989376.gif'), ('cheers', 'https://cdn.discordapp.com/emojis/821658747834204211.gif'), ('hugs', 'https://cdn.discordapp.com/emojis/821658748979380245.gif'), ('transformation', 'https://cdn.discordapp.com/emojis/821658751810797568.gif'), ('icespirit', 'https://cdn.discordapp.com/emojis/821658751961792512.gif')]
    self.decks = data = ['https://link.clashroyale.com/deck/en?deck=26000059;26000014;26000011;28000014;27000002;28000011;26000019', 'https://link.clashroyale.com/deck/en?deck=26000033;26000060;26000083;26000043;28000008;26000005;28000016;28000002', 'https://link.clashroyale.com/deck/en?deck=28000001;28000000;27000006;28000010;26000037;26000027;26000038;26000010', 'https://link.clashroyale.com/deck/en?deck=26000083;28000007;26000085;28000012;28000015;26000027;27000001;26000039', 'https://link.clashroyale.com/deck/en?deck=26000050;26000061;28000000;26000042;26000024;27000006;26000084;28000011', 'https://link.clashroyale.com/deck/en?deck=28000001;27000012;26000011;26000080;26000057;26000029;26000032;26000037', 'https://link.clashroyale.com/deck/en?deck=26000055;27000013;28000001;28000017;26000037;26000050;26000061;26000039', 'https://link.clashroyale.com/deck/en?deck=26000011;26000021;27000006;28000014;26000031;26000064;28000011;26000010', 'https://link.clashroyale.com/deck/en?deck=26000042;26000083;26000051;26000004;26000027;28000015;28000000;26000046', 'https://link.clashroyale.com/deck/en?deck=26000011;26000014;27000002;26000019;28000015;26000054;26000059;28000014', 'https://link.clashroyale.com/deck/en?deck=26000013;26000043;26000038;28000011;28000000;26000051;26000037;26000050', 'https://link.clashroyale.com/deck/en?deck=26000055;26000083;26000061;28000001;28000017;26000032;26000006;26000052', 'https://link.clashroyale.com/deck/en?deck=26000011;27000002;28000009;28000017;26000037;28000010;26000031;26000019', 'https://link.clashroyale.com/deck/en?deck=28000000;28000011;26000061;26000083;26000027;27000012;26000024;26000039', 'https://link.clashroyale.com/deck/en?deck=26000055;26000016;26000005;28000001;28000008;26000032;26000058;26000014', 'https://link.clashroyale.com/deck/en?deck=26000010;26000062;28000011;27000013;26000011;27000006;28000012;26000031', 'https://link.clashroyale.com/deck/en?deck=28000007;26000051;26000042;26000046;28000017;26000004;26000015;26000025', 'https://link.clashroyale.com/deck/en?deck=28000000;28000015;26000083;26000061;26000024;27000012;26000027;26000039', 'https://link.clashroyale.com/deck/en?deck=26000055;28000010;26000048;28000001;28000017;26000042;26000061;26000052', 'https://link.clashroyale.com/deck/en?deck=26000085;28000007;26000037;28000012;26000027;27000012;26000083;28000015', 'https://link.clashroyale.com/deck/en?deck=26000010;26000031;26000011;28000011;28000000;27000008;26000001;27000006', 'https://link.clashroyale.com/deck/en?deck=28000001;26000049;26000013;26000048;26000009;28000013;26000016;26000052', 'https://link.clashroyale.com/deck/en?deck=26000084;26000024;26000039;26000061;26000027;28000007;28000015;26000083', 'https://link.clashroyale.com/deck/en?deck=26000031;26000011;26000021;27000006;28000011;28000014;26000064']
  @commands.Cog.listener()
  async def on_member_join(self, member: discord.Member):
   for guild in self.bot.guilds:
     if guild.id == 876900213938356244:
        channel = guild.get_channel(876900213938356247)
        guild = guild
   embed = discord.Embed(color = int('FFA500', 16), description=f'Welcome to {guild.name}!\nPlease abide by the rules listed in <#877061646126809148> and set yourself up through <#877056352441229322>.\nThank you:)')
   await channel.send(content = f'{member.mention}', embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
