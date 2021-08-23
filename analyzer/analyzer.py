from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import MaxRetryError
from selenium.webdriver.common.keys import Keys
import selenium
from seleniumrequests import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import asyncio
from PIL import Image

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
        self.all_decks = []
        self.counter = 0
        self.pages = 0
        self.decks = 0
    
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
         password.send_keys(self.password)
         login_button.click()
         try:
          re = self.driver.find_element_by_id('challenge_response')
          re.send_keys(self.user)
          bt1 = self.driver.find_element_by_id('email_challenge_submit')
          bt1.click()
         except NoSuchElementException as e:
             await self.channel.send(e)
        except NoSuchElementException as e:
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
        except NoSuchElementException as e:
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
        for deck in listX:
            if counter%2==0:
             counter = counter+1
             url = deck['href']
             self.all_decks.append(url)
            else:
             counter = counter+1
             continue
        if len(self.all_decks) == 0:
            return await ctx.send("No data was found")

        if self.counter != 0:
         if self.counter == self.pages:
             answer = await self.yesORno(ctx)
             if not answer:
               all_decks_without_repetition = set(self.all_decks)
               for i in all_decks_without_repetition:
                    count = self.all_decks.count(str(i))
                    await self.image(ctx, i, count)
             else:
                  list_of_files = []
                  list_of_images = []
                  all_decks_without_repetition = set(self.all_decks)
                  for i in all_decks_without_repetition:
                    count = self.all_decks.count(str(i))
                    fileName = await self.pdf(ctx, i, count)
                    list_of_files.append(fileName)
                  for i in range(0, len(list_of_files)):
                      img = Image.open(list_of_files[i])
                      list_of_images.append(img.convert('RGB'))
                  rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
                  rgb.save(r'all_decks_with_pgNO.pdf',save_all=True, append_images=list_of_images)
                  await ctx.send(file=discord.File('all_decks_with_pgNO.pdf'))
                  
             self.driver.quit()
             return

         elif self.counter == self.decks:
             answer = await self.yesORno(ctx)
             if not answer:
              decks = []
              for N in range(0, self.decks):
                  decks.append(self.all_decks[N])
              all_decks_no_repetition = set(decks)
              for i in all_decks_no_repetition:
                    count = decks.count(str(i))
                    await self.image(ctx, i, count)
             else:
                  decks = []
                  list_of_files = []
                  list_of_images = []
                  for N in range(0, self.decks):
                   decks.append(self.all_decks[N])
                  all_decks_no_repetition = set(decks)
                  for i in all_decks_no_repetition:
                    count = decks.count(str(i))
                    fileName = await self.pdf(ctx, i, count)
                    list_of_files.append(fileName)

                  for i in range(0, len(list_of_files)):
                      img = Image.open(list_of_files[i])
                      list_of_images.append(img.convert('RGB'))
                  rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
                  rgb.save(r'all_decks_with_dNO.pdf',save_all=True, append_images=list_of_images)
                  await ctx.send(file=discord.File('all_decks_with_dNO.pdf'))                 

             self.driver.quit()
             return

        self.counter = self.counter + 1                    
        if self.counter == 1:
            await self.pagesORdecks(ctx) 
            if self.pages != 0:
             self.message = await ctx.send(content = f"Analyzer's current progress: {str((self.counter/self.pages*100))}%")
            else:
             self.message = await ctx.send(content = f"Analyzer's current progress: {str((self.counter/self.decks*100))}%")

        try:
            if self.pages != 0:
             percent = (self.counter/self.pages*100)
             if percent > 100.0:
                 percent = 100.0
             await self.message.edit(content = f"Analyzer's current progress: {str(percent)}%")
            elif self.decks != 0:
             percent = (self.counter/self.decks*100)
             if percent > 100.0:
                 percent = 100.0
             await self.message.edit(content = f"Analyzer's current progress: {str(percent)}%")

            nextButton = self.driver.find_element_by_xpath('//*[@id="page_content"]/div[7]/div/a[3]')
            nextButton.send_keys(Keys.ENTER)
            time.sleep(1)
            try:
                await self.txt(ctx, self.driver.page_source)
            except Exception as e:
                await self.channel.send(e)
        except Exception as ex:
             await self.channel.send(ex)
             self.restartdriver(ctx)
             return await ctx.send("please try again")


    async def yesORno(self, ctx):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send("Do you want a pdf of the images?")
        try:
         msg = await self.bot.wait_for('message', timeout=60, check=check)
         if msg.content.lower() == 'yes':
             return True
         else:
             return False
        except TimeoutError:
            return False

    async def pagesORdecks(self, ctx):
        await ctx.send("```py\nPlease enter the number of pages or total number of recent decks to be tracked.\n`pages 10` for last 10 pages\n`decks 10`for last 10 decks.\nOnly one of them can be used at a time.```")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        msg = await self.bot.wait_for('message', timeout = 60, check=check)
        input = msg.content
        try:
            if 'pages' in input:
                input = input.replace('pages', '').replace(' ', '')
                try:
                 self.pages = int(input)
                except ValueError:
                 return await ctx.send('Invalid value. Try again.')
            elif 'decks' in input:
                input = input.replace('decks', '').replace(' ', '')
                try:
                 self.decks = int(input)
                except ValueError:
                 return await ctx.send('Invalid value. Try again.')
            else:
                return await ctx.send('Invalid option.')

        except TimeoutError:
            self.pages = 1
            return await ctx.send("Timeout.\nContinuing with pages 1 by default")


    async def image(self, ctx, url:str, count: int):
        deck = self.bot.get_cog("Deck")
        await deck.only_deck_image(ctx, url, count)
    async def pdf(self, ctx, url:str, count: int):
        deck = self.bot.get_cog("Deck")
        return await deck.only_deck_pdf(ctx, url, count)

    @commands.command()
    async def analyze(self, ctx, tag: str, battletype: str):
        """tag - Clash Royale Player Tag
        battletype(options) - gc, cc, ladder, clan1v1, 2v2, friendly, gt"""
        self.clear_old_cache()
        tag = self.formatTag(tag=tag)
        if self.verifyTag(tag=tag) is False:
            return await ctx.send("Invalid tag")
        bID = self.getBattleID(ctx, battletype)
        if len(bID) == 0:
            return await ctx.send(f'{ctx.author.mention} That is an invalid option.\nAvailable options: gc, cc, ladder, clan1v1, 2v2, friendly, gt')
        else:
            try:
             try:
              self.restartdriver(ctx)
              self.driver.get(url=f'https://royaleapi.com/player/{tag}/battles/history?battle_type={bID}')
              await self.txt(ctx, self.driver.page_source)
             except MaxRetryError:
                self.driver.close()
                reloader = self.bot.get_command('reload')
                await ctx.invoke(reloader, 'analyzer')
                self.__init__(self.bot)
                await ctx.send("Restarting analyzer..")
                await self.restartdriver(ctx)
                await self.analyze(ctx, tag, battletype)                
            except AttributeError:  
                self.__init__(self.bot)
                await ctx.send("Restarting analyzer..")
                await self.restartdriver(ctx)
                await self.analyze(ctx, tag, battletype)
            except Exception as e:
                self.__init__(self.bot)
                await ctx.send("Restarting analyzer..")
                await self.restartdriver(ctx)
                await self.analyze(ctx, tag, battletype) 
                await self.channel.send(e)



    @commands.command()
    async def startdriver(self, ctx):

            self.browser()
            await self.credentials()
            await self.login()
            await self.authorize()
            await ctx.tick()
    @commands.command()
    async def restartdriver(self, ctx):
         try:
            self.driver.quit()
            self.browser()
            await self.credentials()
            await self.login()
            await self.authorize()
            await ctx.tick()
         except AttributeError:
             await self.startdriver(ctx)
    
    def clear_old_cache(self):
        self.all_decks.clear()
        self.counter = 0
        self.pages = 0
        self.decks = 0
