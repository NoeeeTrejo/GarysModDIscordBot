# bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
from pyppeteer import launch
from zipfile import ZipFile
from pathlib import Path
import shutil
import glob


load_dotenv()
TOKEN = 'INSERT_TOKEN_HERE'
prefix = '.GMOD'
path_to_GMOD = ""
path_to_maps = path_to_GMOD + '/maps'
path_to_addons = path_to_GMOD + '/addons'
path_to_downloads = 'C:/Users/pineapple/Downloads'
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    global session_reads
    session_reads = '```\n'


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    if message.content.startswith(prefix):
        global session_reads
        rest =  message.content.split(prefix)[1]

        if 'get-all' in rest: 
            messages = set(filter(lambda msg: msg.content.startswith(prefix) and 'id=' in msg.content, await message.channel.history(limit=200).flatten()))
            
            # Open Browser and prepare to type links into box
            browser = await launch({'headless': False})
            page = await browser.newPage()
            await page.goto('https://steamworkshopdownloader.io/')
            for i in range(10): 
                await page.keyboard.press('Tab') #navigate to typing area
            response = "```"
            
            #Grab what's currently in the workshop.lua file, so we don't redownload the same thing
            f = open(path_to_GMOD + 'workshop.lua', mode='r')
            installed = f.read()
            f.close()
            f = open(path_to_GMOD + 'workshop.lua', mode='w')
            maps = set() #A set of links for maps and skins
            skins = set()

            #Iterate through all mesasages in format '.GMOD ____ <link>'
            for msg in messages: 
                rest =  msg.content.split(prefix)[1] #should give ____ <link> ... <link>
                command, links = rest.split(' ')[1], rest.split(' ')[2:]
                typeDownload = maps if command == 'map' else skins #for organizing into maps and skins
                
                # Go through the links
                for link in links: 
                    id = link.split('id=')[1].split('&')[0]
                    if (id not in installed) and (link not in typeDownload): 
                        typeDownload.add(link)
                        f.write(f"""resource.AddWorkshop ({id})\n""")
                
            f.close()

            if skins:
                for link in skins: 
                    await page.keyboard.type(f'{link} ') 
                    await asyncio.sleep(0.001)

                #Turn on AutoDownload
                for i in range(6): 
                    await page.keyboard.press('Tab')    
                await page.keyboard.press('Enter')
                await asyncio.sleep(40) # waiting 60 min for stuff to download 

                directory = path_to_downloads
                for filename in os.listdir(directory):
                    if filename.endswith(".zip"):
                        path_to_file = os.path.join(directory, filename)
                        with ZipFile(path_to_file, 'r') as zipObj:
                            zipObj.extractall("." + path_to_addons)
                        os.remove(path_to_file)
                            

                #Reload the website and go to type the links
                await page.goto('https://steamworkshopdownloader.io/')
                for i in range(10): 
                    await page.keyboard.press('Tab') #navigate to typing area

            if maps:
                for link in maps: 
                    await page.keyboard.type(f'{link} ') 
                    await asyncio.sleep(0.25)

            
                #Turn on AutoDownload
                for i in range(6): 
                    await page.keyboard.press('Tab')
                await page.keyboard.press('Enter')
                await asyncio.sleep(120) # waiting 2 min for stuff to download 


                #TODO: FIX RECURSIVE SEARCH FOR .BSP
                directory = path_to_downloads
                for filename in os.listdir(directory):
                    if filename.endswith(".zip"):
                        path_to_file = os.path.join(directory, filename)
                        with ZipFile(path_to_file, 'r') as zipObj:
                            zipObj.extractall('.' + path_to_maps)
                        os.remove(path_to_file)

                pathname = '.' + path_to_maps + "/**/*.BSP"
                files = glob.glob(pathname, recursive=True)
                for bsp in files: 
                    os.rename(bsp, '.' + path_to_maps + '/' + bsp.split('\\')[-1])
                
                print("finished moving over bsp files")

                for filename in os.listdir('.' + path_to_maps):
                    print("attempting to rm left over folders")
                    shutil.rmtree('.' + path_to_maps + '/' + filename)
                
            await browser.close()



        elif 'fix-no-prefix' in rest: 
            messages = set(filter(lambda msg: (not msg.content.startswith(prefix)) and 'id=' in msg.content, await message.channel.history(limit=200).flatten()))
            for msg in messages: 
                response =  prefix + msg.content
                await msg.channel.send(response) #send updated version
                await msg.delete()

        elif 'clear-dupes' in rest: 
            messages = list(filter(lambda msg: not msg.content.startswith(prefix) and 'id=' in msg.content, await message.channel.history(limit=200).flatten()))
            seen = set()
            count = 0
            for msg in messages: 
                if msg not in seen: 
                    seen.add(msg)
                else: 
                   await msg.delete()
                   count += 1
            await messages[0].channel.send(f"Cleared {count} messages!") #too lazy to set a channel, so I just index into the first msg and use it's channel to send a response


client.run(TOKEN)
