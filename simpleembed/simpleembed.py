import discord
from redbot.core import commands
from redbot.core import checks
from typing import Optional


class SimpleEmbed(commands.Cog):
	"""Simply send embeds."""
	def __init__(self, bot):
		self.bot = bot
	
	@checks.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(embed_links=True)
	@commands.command()
	async def sendembed(self, ctx, color: Optional[discord.Color]=None, *, text):
		"""
		Send an embed.
		
		Use the optional parameter `color` to change the color of the embed.
		The embed will contain the text `text`.
		All normal discord formatting will work inside the embed.
		Send the optional image with the command to insert an image at the bottom of the embed.
		"""
		if color is None:
			color = await ctx.embed_color()
		embed = discord.Embed(
			description=text,
			color=color
		)
		if ctx.message.attachments:
			content = await ctx.message.attachments[0].to_file()
			embed.set_image(url="attachment://" + str(content.filename))
		await ctx.send(embed=embed, file=content if ctx.message.attachments else None)
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass

	async def red_delete_data_for_user(self, **kwargs):
		"""Nothing to delete."""
		return

	@commands.command()
	async def shop(self, ctx):
		embed = discord.Embed(title="Invite", url = "https://discord.gg/nKarkppYsy", description = "🛒The Shop🛒", color = 0x00ff59)
		embed.set_author(name="Chiefs United!", url="https://discord.gg/nKarkppYsy", icon_url="https://media.discordapp.net/attachments/819989548879708171/823505579691474954/download.png")
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/754780357349605467/760462448846831646/image1.png?width=473&height=473")
		embed.add_field(name="!!buy 1 - Add custom emoji to your name", value="50k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 2 - Make your own custom command", value="50k Chiefs Coins", inline =False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 3 - Buy Rare role", value="60k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 4 - Buy Epic Role [rare req]", value= "75k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 5 - Buy Legendary Role [epic req]", value="1M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 6 - Buy Pass Royale [leggy req]", value="10M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!!buy 7 - Buy Nitro Classic [leggy req]", value="10M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.set_footer(text="\t \t *Bot by Gladiator#0004")
		await ctx.send(embed = embed)
