from discord import message
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

    async def getBattleID(self, ctx, name: str):
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
            return await ctx.send(f'{ctx.author.mention} That is an invalid option.\nAvailable options: gc, cc, ladder, clan1v1, 2v2, friendly, gt')   

    def verifyTag(tag):
        """Check if a player's tag is valid"""
        check = ["P", "Y", "L", "Q", "G", "R", "J", "C", "U", "V", "0", "2", "8", "9"]
        if len(tag) > 15:
            return False
        if any(i not in check for i in tag):
            return False
        return True

    def formatTag(tag):
        """Sanitize and format CR Tag"""
        return tag.strip("#").upper().replace("O", "0")    
    
    async def txt(self, ctx, html:str):
        counter = 2
        s = bs(html)
        listX = s.find_all('a', class_='button_popup item', href = True)
        for deck in listX:
            if counter%2==0:
             counter = counter+1
             url = deck['href']
             await self.image(ctx, url)
             await asyncio.sleep(1)
            else:
             counter = counter+1
             continue

    async def image(self, ctx, url:str):
        deck = self.bot.get_cog("Deck")
        await deck.only_deck_image_1(ctx, url)

    @commands.command()
    async def analyze(self, ctx, tag: str, battletype: str):
        """Analyzer OP"""
        tag = self.formatTag(tag)
        if self.verifyTag(tag) is False:
            return await ctx.send("Invalid tag")
        battletype = self.getBattleID(ctx, battletype)
        self.driver.get(url=f'https://royaleapi.com/player/{tag}/battles/history?battle_type={battletype}')
        await self.txt(ctx, self.driver.page_source)

    @commands.command()
    async def startdriver(self, ctx):
            await ctx.tick()
            self.browser()
            await self.credentials()
            await self.login()
            await self.authorize()
            await ctx.send("Started")
