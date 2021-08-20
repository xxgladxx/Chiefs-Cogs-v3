#importing modules
import discord
import clashroyale
from redbot.core import checks, commands
import urllib.request
import requests
from bs4 import BeautifulSoup
import asyncio

credits = 'Gladiator#2979'

    #main class
class ClashUtils(commands.Cog):
        """Set of some helpful clash royale utilities."""

        def __init__(self, bot):
            self.bot = bot
            self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            self.rplayer_url ='https://royaleapi.com/player'
            self.deck = bot.get_cog("Deck")

        def strip(self, tag: str):
            tag = tag.strip('#')
            tag = tag.replace('O', '0')
            tag = tag.upper()
            return tag
        
        async def initialize(self):
            token = await self.bot.get_shared_api_tokens("clashroyale")
            token = token["api_key"]
            self.clash =  clashroyale.official_api.Client(token=token['token'], is_async=True, url="https://proxy.royaleapi.dev/v1")

        @commands.command(name = 'analytics', aliases = ['analyze','track'])
        async def _analytics(self, ctx, tag: str, time: str):
            """Get all Card Usage% and Win% of any player
            tag = clash royale player tag
            time = time interval to track data. Available options: 1, 3, 7, 14"""
            if len(time) == 0:
                return await ctx.send("```Please also tell the time interval for analytics while using the command.\nAvailable options: 1, 3, 7, 14.```")
            elif time not in ['1', '3', '7', '14']:
                return await ctx.send("```Invalid value for time interval.\nAvailable options: 1, 3, 7, 14```")

            tag = self.strip(tag)
            url = f"{self.rplayer_url}/{tag}/analytics?time={time}d"
            result = requests.get(url, headers=self.headers)
            data = result.content.decode('utf-8')
            soup = BeautifulSoup(data)
            cards = soup.find_all('td', class_='mobile-hide')
            all_cards = []
            all_rates = []
            for card in cards:
                all_cards.append(card.text)
            useP = soup.find_all('td', class_='right aligned')
            counter1 = 0
            output = ""
            for us in useP:
                if '%' in us.text:
                    ut = us.text.replace('\n', '')
                    if len(ut) == 2:
                        ut=f"0{ut}"
                    if counter1 %2 == 0:
                        output = f"{ut}"
                        counter1 = counter1+1
                    elif counter1 % 2 != 0:
                        output = f"{output}\t{ut}"
                        all_rates.append(output)
                        output = ""
                        counter1 = counter1+1
            result = ""
            result1= ""
            result2 = ""
            spaces = ""
            for i in range(0, len(all_cards)):
                pos = str(i+1)
                if len(pos) == 1:
                    pos = f"0{pos}"
                card = all_cards[i]
                spacing = 17-len(card)
                for space in range(1, spacing):
                    spaces = f"{spaces} "
                if len(result) + len(f"{result}\n{pos}. {card}{spaces}\t{all_rates[i]}") <= 2000:
                    result = f"{result}\n{pos}. {card}{spaces}\t{all_rates[i]}"
                elif len(result) + len(f"{result}\n{pos}. {card}{spaces}\t{all_rates[i]}") <= 4000:
                    result1 = f"{result1}\n{pos}. {card}{spaces}\t{all_rates[i]}"
                else:
                    result2 = f"{result2}\n{pos}. {card}{spaces}\t{all_rates[i]}"
                spaces = ""
            header = f"Sno.  | Card Name | \t|U%|\t|W%|"
            await ctx.send(f"```{header}\n{result}```")
            if len(result1) is not 0:
             await ctx.send(f"```{result1}```")
            if len(result2) is not 0:
             await ctx.send(f"```{result2}```")
            #await ctx.invoke(self.bot.get_command('margin'))
            await ctx.tick()

        @commands.command(name='recentdecks', aliases=['rd'])
        async def _recentdecks(self, ctx, tag:str):
            """Shows the recent decks used for a player"""
            tag = self.strip(tag)
            url = f"{self.rplayer_url}/{tag}/decks"
            result = requests.get(url, headers=self.headers)
            data = result.content.decode('utf-8')
            soup = BeautifulSoup(data)
            decks = soup.find_all('a', class_='button_popup item', href=True)
            for deck in decks:
                url = deck['href']
                await ctx.send(url)
                await asyncio.sleep(2.5)  
            await ctx.tick()

        @commands.command(name='deckimage', aliases=['img'])
        async def _deckimage(self, ctx, url:str):
            """Shows only the image for the entered deck link"""
            deck = self.bot.get_cog("Deck")
            try:
                await deck.only_deck_image(ctx, url)             
            except Exception as e:
                return await ctx.send(e)

        @commands.command(name='duelchecker', aliases=['dc', 'duelcheck'])
        async def _duelchecker(self, ctx):
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
                    await ctx.send(f"Cards repeated include:\n```{output}```")  
            
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
                    await ctx.send(f"Cards repeated include:\n```{output}```")       
            else: 
                await ctx.send("Try again with 2 or 3 deck links.")
