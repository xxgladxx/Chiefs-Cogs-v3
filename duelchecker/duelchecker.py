import discord
from discord.ext.commands.core import check
from redbot.core import commands

class DuelChecker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.deck = bot.get_cog('Deck')

    @commands.command()
    async def checker(self, ctx):
        """Helps with checking if any card is repeated in duel decks"""
        await ctx.send(f"{ctx.author.mention}, please send the deck links separated with a comma {0} followed by a space.\nfor eg: decklink1, decklink2, decklink3".format('(,)'))
        def check(m):
             return m.channel == ctx.channel and m.author == ctx.author
            
        msg = await self.bot.wait_for('message',  timeout=120, check = check)
        message = msg.content
        decklink_1 = message[0:message.index(', ')] 
        message = message[message.index(decklink_1):len(message)]
        decklink_2 = message[0:message.index(', ')]
        message = message[message.index(decklink_2):len(message)]
        decklink_3 = message
        keys_1 = self.deck.decklink_to_cards(decklink_1)
        keys_2 = self.deck.decklink_to_cards(decklink_2)
        keys_3 = self.deck.decklink_to_cards(decklink_3)
        await ctx.send(keys_1)
        await ctx.send(keys_2)
        await ctx.send(keys_3)
    
