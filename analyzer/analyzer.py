from discord import message
from discord.ext.commands.core import check
import selenium
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import asyncio

import discord
from redbot.core import commands

class Analyzer(commands.Cog):
    """Bunch of cool utilites"""

    def __init__(self, bot):
        self.bot = bot
        for guild in self.bot.guilds:
            if guild.id == 875615868166475776:
                self.channel = guild.get_channel(878968502365618186)
        self.cmd = self.bot.get_command('image')
    
    def browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--enable-javascript")
        user = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        chrome_options.add_argument(f"user-agent={user}")
        chrome_options.add_argument('window-size=1200x600')
        self.driver = Chrome(ChromeDriverManager().install(), options=chrome_options)
        return

    async def credentials(self):
        creds = await self.bot.get_shared_api_tokens('tw_credentials')
        self.user = creds['un']
        self.password = creds['pw']
        return
    
    async def login(self):
        self.driver.get(url='https://royaleapi.com/login/twitter?r=/player/2CG2RLUV/battles/history?battle_type=clanMate')
        time.sleep(5)
        self.driver.get_screenshot_as_file('step1.png')
        await self.channel.send(file=discord.File('step1.png'))
        email = self.driver.find_element_by_id('username_or_email')
        password = self.driver.find_element_by_id('password')
        login_button = self.driver.find_element_by_id('allow')
        try:
         email.send_keys('CRIndiaBot')
         password.send_keys('Gladiatorisgod')
         login_button.click()
        except selenium.common.exceptions.NoSuchElementException as e:
            await self.channel.send(e)
        except Exception as e:
            await self.channel.send(e)
        self.driver.get_screenshot_as_file('step2.png')
        await self.channel.send(file=discord.File('step2.png'))
        time.sleep(2)
        return
    
    async def authorize(self):
        try:
          auth_button = self.driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
          auth_button.click()
        except selenium.common.exceptions.NoSuchElementException as e:
            await self.channel.send(e)
        except Exception as e:
            await self.channel.send(e)
        self.driver.get_screenshot_as_file('step3.png')
        await self.channel.send(file=discord.File('step3.png'))
        return

    def getBattleID(self, ctx, name: str):
        if name.lower() == 'gc':
            return 'challenge-grand'
        elif name.lower() == 'cc':
            return 'challenge-classic'
        elif name.lower() == 'ladder':
            return 'PvP'
        elif name.lower() == 'clan1v1':
            return 'clanMate'
        elif name.lower() == '2v2':
            return 'clanMate2v2'
        elif name.lower() == 'friendly':
            return 'friendly'
        elif name.lower() == 'gt':
            return 'global-tournament'       
        else:
            return ''   

    def verifyTag(self, tag):
        """Check if a player's tag is valid"""
        check = ["P", "Y", "L", "Q", "G", "R", "J", "C", "U", "V", "0", "2", "8", "9"]
        if len(tag) > 15:
            return False
        if any(i not in check for i in tag):
            return False
        return True

    def formatTag(self, tag):
        """Sanitize and format CR Tag"""
        return tag.strip("#").upper().replace("O", "0")    
    
    async def txt(self, ctx, html:str):
        counter = 2
        s = bs(html)
        listX = s.find_all('a', class_='button_popup item', href = True)
        all_decks = []
        for deck in listX:
            if counter%2==0:
             counter = counter+1
             url = deck['href']
             all_decks.append(url)
            else:
             counter = counter+1
             continue
        if len(all_decks) == 0:
            return await ctx.send("No data was found")
        all_decks_without_repetition = set(all_decks)
        # file = open("X.py", 'w+')
        # file.write(f'Repeated:\n{all_decks}')
        # file.close()
        # await ctx.send(file=discord.File('X.py'))
        # file = open("X.py", 'w+')
        # file.write(f'Non Repeated:\n{all_decks_without_repetition}')
        # file.close()
        # return await ctx.send(file=discord.File('X.py'))
        for i in all_decks_without_repetition:
            count = all_decks.count(str(i))
            await self.image(ctx, i, count)
            await asyncio.sleep(1)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        msg = await self.bot.wait_for('message', timeout=60, check = check)
        if msg.content.lower() == 'yes':
            nextButton = self.driver.find_element_by_xpath('//*[@id="page_content"]/div[7]/div/a[3]')
            nextButton.click()
            try:
                await self.txt(ctx, self.driver.page_source)
            except Exception as e:
                return self.channel.send(e)


            

        

    async def image(self, ctx, url:str, count: int):
        deck = self.bot.get_cog("Deck")
        await deck.only_deck_image(ctx, url, count)

    @commands.command()
    async def analyze(self, ctx, tag: str, battletype: str):
        """tag - Clash Royale Player Tag
        battletype(options) - gc, cc, ladder, clan1v1, 2v2, friendly, gt"""
        tag = self.formatTag(tag=tag)
        if self.verifyTag(tag=tag) is False:
            return await ctx.send("Invalid tag")
        bID = self.getBattleID(ctx, battletype)
        if len(bID) == 0:
            return await ctx.send(f'{ctx.author.mention} That is an invalid option.\nAvailable options: gc, cc, ladder, clan1v1, 2v2, friendly, gt')
        else:
            try:
             self.driver.get(url=f'https://royaleapi.com/player/{tag}/battles/history?battle_type={bID}')
             await self.txt(ctx, self.driver.page_source)
            except AttributeError:
                if self.channel is None:
                 self.__init__(self.bot)
                await ctx.send("Restarting analyzer..")
                await self.startdriver(ctx)
                await self.analyze(ctx, tag, battletype)


    @commands.command()
    async def startdriver(self, ctx):

            self.browser()
            await self.credentials()
            await self.login()
            await self.authorize()
            await ctx.tick()
    
