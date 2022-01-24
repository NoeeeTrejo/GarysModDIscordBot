# GarysModDIscordBot
A Discord Bot I made, for making it easier for my friend to add addons to his Gary's Mod Server.

## TLDR (How it works/What is it?):

A Discord Bot that uses discord to be a place to paste Steam Workshop links. Steam workshops are downloaded in batches, the user who runs the server (or anyone), can run a command that goes through all the discord messages in the channel, and adds all workshop links that aren't already installed. 

## How to use: 
* for  skins do: .GMOD skin <link(s)>
* for maps do: .GMOD map <link(s)>
* For getting them all: do .GMOD get-all

## Requirements:
pyppeteer - For controlling a browser (For downloading the steam workshop assets)
discord.py - For running the Discord Bot
python-dotenv  - For getting environment variables
asyncio - For waiting for certain actions to happen, or timeouts
pathlib - For directory stuff
glob2 - For directory stuff
zipfile - Unzipping files that are downloaded 

## Why did I make this? 

My friend has a [Garry's Mod](https://store.steampowered.com/app/4000/Garrys_Mod/) Server that he hosts, so that our discord friends can all join and play games together on our own private server. Anyway, the game allows users to have custom skins by downloading them from the Steam Workshop, but it can get quite tideous when it's a lot of skins, maps, objects, etc. So, I made a discord bot that is able to do all of this! Anyway, it made his life so much easier, and made it so all our discord friends could simply type a command into the discord channel, and we all just put in the things we want, and my friend uses a single command for getting all the skins/maps/objects, and they all get downloaded, extracted, and organized into their respective folder!

## Why is the code so sloppy? 

Honestly, I never intended on uploading this to github or for the code to be seen by anyone, I just kind of wanted to do it without putting much effort into it, it was just like a hot-fix to a problem that my friend was having. 

