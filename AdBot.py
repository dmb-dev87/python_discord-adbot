import discord
from discord.ext import commands
from discord.ext import tasks
from discord import Message
from discord import DMChannel
import json
import asyncio
import base64
import os
import time
import requests
from requests.structures import CaseInsensitiveDict
import ctypes
from colorama import Fore, Back, Style
from colorama import init
init()

r = Fore.RED
g = Fore.GREEN
w = Fore.WHITE



          
adbot = f"""

                                        {r}█████{w}╗ {r}██████{w}╗ {r}██████{w}╗  {r}██████{w}╗ {r}████████{w}╗
                                       {r}██{w}╔══{r}██{w}╗{r}██{w}╔══{r}██{w}╗{r}██{w}╔══{r}██{w}╗{r}██{w}╔═══{r}██{w}╗╚══{r}██{w}╔══╝
                                       {r}███████{w}║{r}██{w}║  {r}██{w}║{r}██████{w}╔╝{r}██{w}║   {r}██{w}║   {r}██{w}║   
                                       {r}██{w}╔══{r}██{w}║{r}██{w}║  {r}██{w}║{r}██{w}╔══{r}██{w}╗{r}██{w}║   {r}██{w}║   {r}██{w}║   
                                       {r}██{w}║  {r}██{w}║{r}██████{w}╔╝{r}██████{w}╔╝╚{r}██████{w}╔╝   {r}██{w}║   
                                       {w}╚═╝  ╚═╝╚═════╝ ╚═════╝  ╚═════╝    ╚═╝

      {Fore.CYAN}                       ╔═════════════════════════[{Style.RESET_ALL}AdBot{Fore.CYAN}]════════════════════════╗
                             ║ {Fore.MAGENTA}Version: {Style.RESET_ALL}1.1{Fore.CYAN}                                           ║
                             ║ {Fore.MAGENTA}Created By: {Style.RESET_ALL}Daddy Lazarus{Fore.CYAN}                              ║
      {Fore.CYAN}                       ╚════════════════════════════════════════════════════════╝
      
      
"""
ctypes.windll.kernel32.SetConsoleTitleW("Loading AdBot...")
with open('config.json', "rb") as infile:
    config = json.load(infile)
    token = config["userdata"].get('token')
    channelids = config["userdata"].get('channelids')
    minutes = config["userdata"].get('minutes')
    timedelay = config["userdata"].get('delay')

if token == "null":
    os.system('cls')
    unset = True
    while unset == True:
        print(Fore.RED + "Error: " + Style.RESET_ALL + "No local userdata found!")
        token = input("Please enter your discord token: ")
        url = "https://canary.discord.com/api/v9/users/@me"

        headers = CaseInsensitiveDict()
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        headers["authorization"] = token

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            while unset == True:
                try:
                    minutes = int(input("Minutes: "))
                    oldmessagevalue = config["userdata"].get('message')
                    oldtimedelay = config["userdata"].get('delay')
                    oldchannelidsvalue = config["userdata"].get('channelids')
                    update = {"userdata": {"token": token,"minutes": minutes, "delay": oldtimedelay, "message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                    config.update(update)
                    with open('config.json', "w") as jsfile:
                        json.dump(config, jsfile)
                        jsfile.close()
                    unset = False
                except:
                    print(Fore.RED + "Error: " + Style.RESET_ALL + "Must be integer value!")
        else:
            print(Fore.RED + "Error: " + Style.RESET_ALL + "Invalid token!")
else:
    pass


ABT = commands.Bot(command_prefix = "?", self_bot=True, loop=None)

@ABT.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW("AdBot v1.1")
    os.system('cls')
    print(adbot + Style.RESET_ALL)
    print('Logged in as ' + Fore.RED + f'{ABT.user.name}#{ABT.user.discriminator}' + Style.RESET_ALL)
    advertise.start()

@tasks.loop(minutes=int(minutes))
async def advertise():
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        channelstosend = config["userdata"].get('channelids')
    if "null" in channelstosend:
        pass
    else:
        for i in channelstosend:
            time.sleep(int(timedelay))
            try:
                # decodedmsg = base64.b64decode(config["userdata"].get('message'))                
                await ABT.get_channel(int(i)).send(config["userdata"].get('message'))
                print(f"{Fore.CYAN}[{Fore.MAGENTA}INFO{Fore.CYAN}]{Style.RESET_ALL} Successfully sent advertisment to channel id '{i}'!")
            except:
                print(f"{Fore.CYAN}[{Fore.MAGENTA}INFO{Fore.CYAN}]{Style.RESET_ALL} Could not send to channel id '{i}', removing from list...")
                with open('config.json', "rb") as infile:
                    config = json.load(infile)
                oldtokenvalue = config["userdata"].get('token')
                oldmessagevalue = config["userdata"].get('message')
                oldchannelidsvalue = config["userdata"].get('channelids')
                oldminutesvalue = config["userdata"].get('minutes')
                oldchannelidsvalue.remove(i)
                update = {"userdata": {"token": oldtokenvalue,"minutes": oldminutesvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                config.update(update)
                with open('config.json', "w") as jsfile:
                    json.dump(config, jsfile)
                    jsfile.close()

@ABT.command()
async def removechannel(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldminutesvalue = config["userdata"].get('minutes')
    oldtimedelay = config["userdata"].get('delay')
    oldchannelidsvalue.remove(id)
    update = {"userdata": {"token": oldtokenvalue,"minutes": oldminutesvalue,"delay": oldtimedelay,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()

@ABT.command()
async def addchannel(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldminutesvalue = config["userdata"].get('minutes')
    oldtimedelay = config["userdata"].get('delay')
    if oldchannelidsvalue == "null":
        update = {"userdata": {"token": oldtokenvalue,"minutes": oldminutesvalue,"delay": oldtimedelay,"message": oldmessagevalue,"channelids": [id]}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    else:
        oldchannelidsvalue.append(id)
        update = {"userdata": {"token": oldtokenvalue,"minutes": oldminutesvalue,"delay": oldtimedelay,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()

@ABT.command()
async def setmsg(ctx, *, msg):
    await ctx.message.delete()
    encodedmsg = str(base64.b64encode(bytes(msg, 'utf-8')))[2:-1]
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldminutesvalue = config["userdata"].get('minutes')
    oldtimedelay = config["userdata"].get('delay')
    update = {"userdata": {"token": oldtokenvalue,"minutes": oldminutesvalue,"delay": oldtimedelay,"message": encodedmsg,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()


ABT.run(token, bot=False)
input()
