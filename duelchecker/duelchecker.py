import discord
from discord.enums import RelationshipType
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
        count = (message.count(', '))

        #To check repetition for 2 decks
        if count == 1:
         repeated = []
         decklink_1 = message[0:message.index(', ')] 
         message = message.replace(decklink_1, '')
         decklink_2 = message
         keys_1 = await self.deck.decklink_to_cards(decklink_1)
         keys_2 = await self.deck.decklink_to_cards(decklink_2)
         x1, x2 = "0", "0"
         for iter in range(0, len(keys_1)):
            card = keys_1[iter]
            if card in str(keys_2):
                x1 = x1 + card
                repeated.append(card)
         if len(x1) == 1 and len(x2) == 1:
            return await ctx.send("**No card** has been repeated!:partying_face:") 
         else:
             output = ""
             for i in range(0, len(repeated)):
                 output = f"{output}\n{repeated[i]}"
             await ctx.send(f"Cards repeated include:\n{output}")  
        
        #To check repetition for 3 decks
        elif count == 2:
         x1, x2 = "0", "0"
         repeated = []
         decklink_1 = message[0:message.index(', ')] 
         message = message[message.index(', ')+1:]
         decklink_2 = message[:message.index(', ')]
         decklink_3 = message.replace(decklink_2, '')  
         keys_1 = await self.deck.decklink_to_cards(decklink_1)
         keys_2 = await self.deck.decklink_to_cards(decklink_2)
         keys_3 = await self.deck.decklink_to_cards(decklink_3)  
         for iter in range(0, len(keys_1)):
            card = keys_1[iter]
            if card in str(keys_2) or card in str(keys_3):
                x1 = x1 + card
                repeated.append(card)
         for iter in range(0, len(keys_1)):
            card = keys_2[iter]
            if card in str(keys_3) and card not in str(repeated):
                x1 = x1 + card
                repeated.append(card)
         if len(x1) == 1 and len(x2) == 1:
            return await ctx.send("**No card** has been repeated!:partying_face:")
         else:
             output = ""
             for i in range(0, len(repeated)):
                 output = f"{output}\n{repeated[i]}"
             await ctx.send(f"Cards repeated include:\n{output}")       



        else: 
            return await ctx.send("Try again with 2 or 3 deck links.")
            
