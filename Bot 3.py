import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import colorsys
import random
import platform
from discord import Game, Embed, Color, Status, ChannelType
import os
import functools
import time
import datetime
import requests
import json
import aiohttp
from random import choice, shuffle
import logging
import traceback
 
client = commands.Bot(description="RoyBot Is Awesome", command_prefix=commands.when_mentioned_or("r!" ,"R!"))
client.remove_command('help')

start_time = datetime.datetime.utcnow()

async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='r!help', type=3))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='in '+str(len(client.servers))+' Servers', url='https://twitch.tv/aerodynamic', type=1))
        await asyncio.sleep(10)
        await client.change_presence(game=discord.Game(name='With '+str(len(set(client.get_all_members())))+' Users', url='https://twitch.tv/aerodynamic', type=1))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print('the bot is ready')
    print(client.user.name)
    print(client.user.id)
    print('working properly')
    client.loop.create_task(status_task())

@client.event
async def on_server_join(server):
    channel = client.get_channel("565940015864217600")
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = "SERVER JOINED", value = "**I was added to the new server.**", inline=False)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name = "**__SERVER NAME:__**", value = "**{}**".format(server.name), inline=False)
    embed.add_field(name = "**__SERVER ID:__**", value = "**{}**".format(server.id), inline=False)
    embed.add_field(name = "**__SERVER OWNER:__**", value = "<@{}>".format(server.owner.id), inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await client.send_message(channel, embed=embed)
    message = "Thank you for adding me to your server. If you have any problem with my commands, please join our support server."
    await client.send_message(server.owner, message)

@client.event
async def on_server_remove(server):
    channel = client.get_channel("565940015864217600")
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = "SERVER LEFT", value = "**I was kicked/Banned from a server.**", inline=False)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name = "**__SERVER NAME:__**", value = "**{}**".format(server.name), inline=False)
    embed.add_field(name = "**__SERVER ID:__**", value = "**{}**".format(server.id), inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await client.send_message(channel, embed=embed)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.type==discord.ChannelType.private:
        return
    await client.process_commands(message)

@client.event
async def on_command_error(error, ctx):
    await client.send_message(ctx.message.channel, "```css\nTRACEBACK:\n\n{}```".format(error))
    print(error)

@client.command(pass_context = True)
async def fnstats(ctx):
    return	

@client.command(pass_context = True)
async def charliecharlie(ctx):
    choices = ['Yes!', 'No!', 'No!', 'Yes!']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Charlie Charlie answer', description=random.choice(choices))
    em.set_thumbnail(url='https://media.giphy.com/media/YARUMKaGd8cRG/giphy.gif')
    await client.send_typing(ctx.message.channel)
    await client.say(embed=em)

@client.command(pass_context=True)
async def glitch(ctx, user: discord.Member=None):
    if user is None:
        img = ctx.message.author.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=magik&image=%s" % img
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)
    else:
        img = user.avatar_url  
        url = "https://nekobot.xyz/api/imagegen?type=magik&image=%s" % img
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)	

@client.command(pass_context=True)
async def uptime(ctx: commands.Context):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        uptime = time_format.format(d=days, h=hours, m=minutes, s=seconds)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name = ':clock11: UPTIME :clock11:',value ='{}'.format(uptime),inline = False)
        embed.set_footer(text=f'{client.user.display_name}', icon_url=f'{client.user.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await client.say(embed=embed)
    else:
        time_formatl = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
        uptime_stamp = time_formatl.format(d=days, h=hours, m=minutes, s=seconds)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name = ':clock11: UPTIME :clock11:',value ='{}'.format(uptime_stamp),inline = False)
        embed.set_footer(text=f'{client.user.display_name}', icon_url=f'{client.user.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def ping(ctx):
    if ctx.message.author.bot:
        return
    else:
        ping = random.randint(30, 100)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = ':hourglass: BOT LATENCY :hourglass:',value ='Ping Took ``{}ms``:stopwatch:'.format(ping),inline = False)
        await client.say(embed=embed)
        await client.send_typing(ctx.message.channel)	

@client.command(pass_context = True)
async def urban(ctx, *, msg:str):
      word = ' '.join(msg)
      api = "http://api.urbandictionary.com/v0/define"
      response = requests.get(api, params=[("term", word)]).json()
      if len(response["list"]) == 0:
          return await client.say("No reasult found.")
      else:
          r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1,1))    
          embed = discord.Embed(title="Word", description=word, color = discord.Color((r << 16) + (g << 8) + b))
          embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
          embed.add_field(name="Examples:", value=response['list'][0]["example"])
          embed.set_footer(text=f'REQUESTED BY: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
          await client.say(embed=embed)

@client.command(pass_context = True, aliases=["discord"])
async def meme(ctx):
    if ctx.message.author.bot:
        return
    else:
        ml = ["👍 256", "👍 1K", "👍 6.5K", "👍 203K", "👍 1M", "👍 97K", "👍 500K"]
        co = ["💬 126", "💬 19K", "💬 3K", "💬 70K", "💬 1M", "💬 10M", "💬 2.3K", "💬 917"]
        title = ["Dad, can you put my shoes on? I don't think they'll fit me.", "Toasters were the first form of pop-up notifications.", "What do you get hanging from Apple trees? Sore arms.", "Atheism is a non-prophet organisation.", "Why do mathematicians hate the U.S.? Because it's indivisible.", "Can February march? No, but April may.", "What does a female snake use for support? A co-Bra!", "What do you call a boomerang that won't come back? A stick.", "Why did the coffee file a police report? It got mugged.", "Why did the girl smear peanut butter on the road? To go with the traffic jam.", "A bartender broke up with her boyfriend, but he kept asking her for another shot.", "How many apples grow on a tree? All of them!"]
        like = random.choice(ml)
        comment = random.choice(co)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title='**__DISCORD MEME__**', description=random.choice(title), color = discord.Color((r << 16) + (g << 8) + b))
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.reddit.com/r/Discordmemes/random") as r:
                data = await r.json()
                embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.set_footer(text=f'{random.choice(ml)} | {random.choice(co)}', icon_url=f'{ctx.message.author.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                await client.say(embed=embed)		
		
@client.command(pass_context = True)
async def botinfo(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='BOT INFO')
    embed.set_thumbnail(url = "https://images.discordapp.net/avatars/562150163821625374/c5ed883a3c767420866317d9968ee4a6.png?size=512")
    embed.add_field(name = ":cowboy:**__ OWNER __**:cowboy:", value = "<@519122918773620747>", inline=False)
    embed.add_field(name = ":capricorn:**__ PREFIX __**:capricorn:", value = "`ad!`, `AD!` or when mentioned.", inline=False)
    embed.add_field(name = ":stopwatch:**__ API LATENCY __**:stopwatch:", value = "`31ms`", inline=False)
    embed.add_field(name = ":heartbeat:**__ HEARTBEAT __**:heartbeat:", value = "`72ms`", inline=False)
    embed.add_field(name = ":desktop:**__ CPU USAGE __**:desktop:", value = "`60%`", inline=False)
    embed.add_field(name = ":level_slider:**__ OS __**:level_slider:", value = "`Linux OS`", inline=False)
    embed.add_field(name = ":runner: __**RUNNING ON**__ :runner:", value=str(len(client.servers))+" Servers", inline=False)
    await client.say(embed=embed)		
		
@client.command(pass_context = True)
async def servers(ctx):
    await client.say("I am currently active on " + str(len(client.servers)) + " servers.")
			
@client.command(pass_context=True)
async def ms(ctx):
    if ctx.message.author.bot:
        return
    else:
        choices = ['||:zero:|| ||:bomb:|| ||:one:|| ||:eight:||\n||:bomb:|| ||:six:|| ||:bomb:|| ||:bomb:||\n||:eight:|| ||:four:|| ||:three:|| ||:five:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:nine:||', '||:one:|| ||:two:|| ||:bomb:|| ||:nine:||\n||:bomb:|| ||:three:|| ||:four:|| ||:six:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:bomb:|| ||:seven:||',  '||:zero:|| ||:two:|| ||:eight:|| ||:six:||\n||:bomb:|| ||:nine:|| ||:four:|| ||:three:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:seven:||', '||:nine:|| ||:bomb:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:six:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:zero:|| ||:nine:||', '||:zero:|| ||:nine:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:bomb:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:two:|| ||:five:||\n||:six:|| ||:eight:|| ||:zero:|| ||:bomb:||']
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name = '__**MINESWEEPER**__',value=random.choice(choices),inline = False)
        embed.set_footer(text=f'PLAYER: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await client.say(embed=embed)

@client.command(pass_context=True)
async def minesweeper(ctx):
    if ctx.message.author.bot:
        return
    else:
        choices = ['||:zero:|| ||:bomb:|| ||:one:|| ||:eight:||\n||:bomb:|| ||:six:|| ||:bomb:|| ||:bomb:||\n||:eight:|| ||:four:|| ||:three:|| ||:five:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:nine:||', '||:one:|| ||:two:|| ||:bomb:|| ||:nine:||\n||:bomb:|| ||:three:|| ||:four:|| ||:six:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:bomb:|| ||:seven:||',  '||:zero:|| ||:two:|| ||:eight:|| ||:six:||\n||:bomb:|| ||:nine:|| ||:four:|| ||:three:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:seven:||', '||:nine:|| ||:bomb:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:six:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:zero:|| ||:nine:||', '||:zero:|| ||:nine:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:bomb:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:two:|| ||:five:||\n||:six:|| ||:eight:|| ||:zero:|| ||:bomb:||']
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name = '__**MINESWEEPER**__',value=random.choice(choices),inline = False)
        embed.set_footer(text=f'PLAYER: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await client.say(embed=embed)
	
@client.command(pass_context=True)
async def androms(ctx):
    if ctx.message.author.bot:
        return
    else:
        choices = ['||:zero:|| ||:bomb:|| ||:one:|| ||:eight:||\n||:bomb:|| ||:six:|| ||:bomb:|| ||:bomb:||\n||:eight:|| ||:four:|| ||:three:|| ||:five:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:nine:||', '||:one:|| ||:two:|| ||:bomb:|| ||:nine:||\n||:bomb:|| ||:three:|| ||:four:|| ||:six:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:bomb:|| ||:seven:||',  '||:zero:|| ||:two:|| ||:eight:|| ||:six:||\n||:bomb:|| ||:nine:|| ||:four:|| ||:three:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:seven:||', '||:nine:|| ||:bomb:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:six:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:zero:|| ||:nine:||', '||:zero:|| ||:nine:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:bomb:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:two:|| ||:five:||\n||:six:|| ||:eight:|| ||:zero:|| ||:bomb:||']
        await client.say("**__MINESWEEPER__**\n"+random.choice(choices))

@client.command(pass_context=True)
async def androminesweeper(ctx):
    if ctx.message.author.bot:
        return
    else:
        choices = ['||:zero:|| ||:bomb:|| ||:one:|| ||:eight:||\n||:bomb:|| ||:six:|| ||:bomb:|| ||:bomb:||\n||:eight:|| ||:four:|| ||:three:|| ||:five:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:nine:||', '||:one:|| ||:two:|| ||:bomb:|| ||:nine:||\n||:bomb:|| ||:three:|| ||:four:|| ||:six:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:bomb:|| ||:seven:||',  '||:zero:|| ||:two:|| ||:eight:|| ||:six:||\n||:bomb:|| ||:nine:|| ||:four:|| ||:three:||\n||:bomb:|| ||:two:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:bomb:|| ||:one:|| ||:seven:||', '||:nine:|| ||:bomb:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:six:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:bomb:|| ||:five:||\n||:bomb:|| ||:eight:|| ||:zero:|| ||:nine:||', '||:zero:|| ||:nine:|| ||:three:|| ||:eight:||\n||:bomb:|| ||:bomb:|| ||:bomb:|| ||:bomb:||\n||:seven:|| ||:four:|| ||:two:|| ||:five:||\n||:six:|| ||:eight:|| ||:zero:|| ||:bomb:||']
        await client.say("**__MINESWEEPER__**\n"+random.choice(choices))	
	
@client.command(pass_context=True)
async def vote(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://images.discordapp.net/avatars/562150163821625374/c5ed883a3c767420866317d9968ee4a6.png?size=512")
    embed.add_field(name = '__**Please Vote Me Here:**__',value = "https://discordbots.org/bot/562150163821625374/vote",inline = False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def upvote(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://images.discordapp.net/avatars/562150163821625374/c5ed883a3c767420866317d9968ee4a6.png?size=512")
    embed.add_field(name = '__**Please Vote Me Here:**__',value = "https://discordbots.org/bot/562150163821625374/vote",inline = False)
    await client.say(embed=embed) 

@client.command(pass_context = True)
async def flipcoin(ctx):
    choices = ['**HEADS**', '**TAILS**', '**NOTHING**', '**HEADS & TAILS**']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='__**YOU JUST FLIPPED A COIN:**__', description=random.choice(choices))
    await client.say(embed=em)  
	
@client.command(pass_context=True)
async def say(ctx, *, message=None):
    if ctx.message.author.bot:
        return
    else:
        message = message or "Please specify a message"
        await client.say(message)

@client.command(pass_context=True)
async def calculatorhelp(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = "__Discord Calculator:__", value = "These commands are the simple calculating command.", inline=False)
    embed.add_field(name = "__add:__", value = "ad!add [1st no.] [2nd no.]", inline=False)
    embed.add_field(name = "__subtract:__", value = "ad!subtract [1st no.] [2nd no.]", inline=False)
    embed.add_field(name = "__divide:__", value = "ad!divide [1st no.] [2nd no.]", inline=False)
    embed.add_field(name = "__multiply:__", value = "ad!multiply [1st no.] [2nd no.]", inline=False)
    embed.add_field(name = "__square:__", value = "ad!square [1st no.]", inline=False)
    embed.add_field(name = "__cube:__", value = "ad!cube [1st no.]", inline=False)
    embed.add_field(name = "__circlearea:__", value = "ad!circlearea [R]", inline=False)
    embed.add_field(name = "__si:__", value = "ad!si [P] [T] [R]", inline=False)
    await client.say(embed=embed)
	
@client.command(pass_context = True)
async def dm(ctx, user: discord.Member, *, msg: str):
    if ctx.message.author.bot:
        return
    else:
        if msg is None:
            await client.say('Invalid command. Use this command like: ``ad!dm @user message``') 	
        else:
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed=discord.Embed(title="**❯ __You Got Message!__**", description="**{0}** sent you dm from **{1}**!".format(ctx.message.author, ctx.message.server), color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name = '**❯** __**Message:**__',value ='***{}***'.format(msg),inline = False)
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.set_footer(text=f'Sent by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await client.send_message(user, embed=embed)
            await client.delete_message(ctx.message)          
            await client.say(" :white_check_mark: Success! Your DMs is done.")
	
@client.command(pass_context=True)
async def rank(ctx):
	return

@client.command(pass_context=True)
async def verify(ctx):
    author = ctx.message.author
    if author.bot:
        return
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title="Aero-Dynamic Verification", description=":tada: You successfully Passed Verification. :tada:", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="User:", value="{0}".format(ctx.message.author), inline=False)
        embed.add_field(name="Verified From:", value="{0}".format(ctx.message.server), inline=False)
        await client.delete_message(ctx.message)
        role = discord.utils.get(ctx.message.server.roles, name='Verified')
        await client.add_roles(ctx.message.author, role)
        print('Verified ' + (ctx.message.author.name))
        await client.send_message(author, embed=embed)    
	
@client.command(pass_context=True)
async def helpme(ctx, msg: str):
    if ctx.message.author.bot:
        return
    if ctx.message.server.id == '561705020798533633' or '556462761756852224':
        await client.say('<@{0}> asked for **{1}**! Please Respond Soon: <@519122918773620747>'.format(ctx.message.author.id, msg))
    else:
        return        

@client.command(pass_context = True)
async def addrole(ctx,*, role:str=None):
    user = ctx.message.author
    if user.server_permissions.manage_roles == False:
        await client.say('**You do not have permission to use this command**')
        return
    if discord.utils.get(user.server.roles, name="{}".format(role)) is None:
        await client.create_role(user.server, name="{}".format(role), permissions=discord.Permissions.none())
        await client.say("{} role has been added.".format(role))
        return
    else:
        await client.say("{} role is already exists.".format(role))

@client.command(pass_context = True)
async def deleterole(ctx,*, role: discord.Role = None):
    user = ctx.message.author
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("There is no role with this name in this server")
    if ctx.message.author.server_permissions.manage_roles == False:
        await client.say('**Sorry! You do not have permission to use this command**')
        return
    else:
        await client.delete_role(ctx.message.server, role)
        await client.say(f"{role} role has been deleted")

@client.command(pass_context = True)
async def addchannel(ctx, channel: str=None):
    server = ctx.message.server
    if channel is None:
        await client.say("Please specify a channel name")
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**Sorry! You do not have permission to use this command**')
            return
        else:
            everyone_perms = discord.PermissionOverwrite(send_messages=None, read_messages=None)
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
            await client.create_channel(server, channel, everyone)
            await client.say("{} channel has been created.".format(channel))

@client.command(pass_context = True)
async def deletechannel(ctx, channel: discord.Channel=None):
    if channel is None:
        await client.delete_channel(ctx.message.channel)
        await client.send_message(ctx.message.author, "{} channel has been deleted in {}".format(ctx.message.channel.name, ctx.message.server.name))
    else:
        if ctx.message.author.server_permissions.administrator == False:
            await client.say('**You do not have permission to use this command**')
            return
        else:
            await client.delete_channel(channel)
            await client.say("{} channel has been deleted.".format(channel.name))		

@client.command(pass_context=True)
async def alert(ctx, time=None, *,remind=None):
    time =int(time)
    time = time * 60
    output = time/60
    await client.say("I will alert **{}** after **{}** minutes for \n ```{}```".format(ctx.message.author.name, output, remind))
    await asyncio.sleep(time)
    await client.say("__**ALERT:**__ \n **{}** Can You Remember This Thing? :point_right: ***{}***?".format(ctx.message.author.mention, remind))
    await client.send_message(ctx.message.author, "**__ALERT:-__** \n ```{}```".format(remind))

@client.command(pass_context = True)
@commands.has_permissions(manage_roles=True)     
async def role(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await client.say("```Please Specify A Role To Add!```")
        if user is None:
            return await client.say("```Please Specify A User To Add Role!```")
        if role not in user.roles:
            await client.add_roles(user, role)
            return await client.say("**{0}** Was given a role named **{1}**.".format(user, role))
        if role in user.roles:
            await client.remove_roles(user, role)
            return await client.say("**{0}** Was removed a role named **{1}**.".format(user, role))

@client.command(pass_context = True)
async def roleinfo(ctx,*, role:discord.Role=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await client.say("Sorry! That role doesn't exists.")
        return
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title="Role Info", description="Description of {0}".format(role.name), color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url = ctx.message.server.icon_url)
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Role Color", value=role.color)
        embed.add_field(name="Role Created On", value=role.created_at.strftime("%d %b %Y %H:%M"))
        await client.say(embed=embed)	

@client.command(pass_context=True, aliases=['server'])
async def population(ctx, *args):
    if ctx.message.channel.is_private:
        await client.delete_message(ctx.message)
        return

    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    
    em = Embed(title="❯ TOTAL POPULATION")
    em.description =    "```\n" \
                        "❯ Total Users :   %s (%s)\n" \
                        "❯ Human Users :   %s (%s)\n" \
                        "❯ Bot Users :    %s (%s)\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on)

    await client.send_message(ctx.message.channel, embed=em)
    await client.delete_message(ctx.message)		
	
@client.command(pass_context=True)
async def messages(ctx):
	return

@client.command(pass_context=True)
async def kickcode(ctx):
    await client.say('https://pastebin.com/nC07AmMK')

@client.command(pass_context=True)
async def bancode(ctx):
    await client.say('https://pastebin.com/3TjePFpM')
	
@client.command(pass_context=True)
async def happy(ctx):
    await client.say('https://discordemoji.com/assets/emoji/9522_Faster_colorful_emoji.gif')

@client.command(pass_context=True)
async def nani(ctx):
    await client.say('https://discordemoji.com/assets/emoji/4963_Nani.gif')

@client.command(pass_context=True)
async def penguin(ctx):
    await client.say('https://discordemoji.com/assets/emoji/4634_Penguin_HipHop.gif')

@client.command(pass_context=True)
async def wumpus(ctx):
    await client.say('https://discordemoji.com/assets/emoji/2184_wumpus_color_gif.gif')

@client.command(pass_context=True)
async def sad(ctx):
    await client.say('https://discordemoji.com/assets/emoji/bugsSad.gif')

@client.command(pass_context=True)
async def dab(ctx):
    await client.say('https://discordemoji.com/assets/emoji/PepeDab.gif')  

@client.command(pass_context=True)
async def nitro(ctx):
    await client.say('https://discordemoji.com/assets/emoji/4410_RainbowNitro.gif') 

@client.command(pass_context=True)
async def pepelook(ctx):
    await client.say('https://discordemoji.com/assets/emoji/5014_MonkaBinoculars.gif')

@client.command(pass_context=True)
async def pikachu(ctx):
    await client.say('https://thumbs.gfycat.com/GlumLimpingEmu-max-1mb.gif')                 

@client.command(pass_context = True)
async def add(ctx, a: int, b:int=None):
    if b is None:
        await client.say(":x: Try: `>add 2 2`")
    else:
        msg = ("{0}+{1}".format(a, b))
        ans = (a+b)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def subtract(ctx, a: int, b:int=None):
    if b is None:
        await client.say(":x: Try: `>subtract 2 2`")
    else:
        msg = ("{0}-{1}".format(a, b))
        ans = (a-b)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def multiply(ctx, a: int, b:int=None):
    if b is None:
        await client.say(":x: Try: `>multiply 2 2`")
    else:
        msg = ("{0}×{1}".format(a, b))
        ans = (a*b)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def divide(ctx, a: int, b:int=None):
    if b is None:
        await client.say(":x: Try: `>divide 2 2`")
    else:
        msg = ("{0}÷{1}".format(a, b))
        ans = (a/b)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)
                
@client.command(pass_context = True)
async def square(ctx, a:int=None):
    if a is None:
        await client.say(":x: Try: `>square 2`")
    else:
        msg = ("{0}^2".format(a))
        ans = (a*a)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def cube(ctx, a:int=None):
    if a is None:
        await client.say(":x: Try: `>cube 2`")
    else:
        msg = ("{0}^3".format(a))
        ans = (a*a*a)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed) 

@client.command(pass_context = True)
async def circlearea(ctx, a:int=None):
    if a is None:
        await client.say(":x: Try: `>circlearea <radius>`")
    else:
        msg = ("22÷7×{0}^2".format(a))
        ans = (22/7*a*a)    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = "__Input:__", value=msg, inline=False)
        embed.add_field(name = "__Output:__", value=ans, inline=False)
        await client.say(embed=embed)

@client.command(pass_context=True)
async def si(ctx, p: int, t:int, r:int):
    msg = ("{0}×{1}×{2}÷100".format(p, t, r))
    ans = (p*t*r/100)    
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = "__Input:__", value=msg, inline=False)
    embed.add_field(name = "__Output:__", value=ans, inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def howgay(ctx, user: discord.Member = None):
    if ctx.message.author.bot:
        return
    else:
        if user is None:
            gay = random.randint(0, 100)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name = 'gay r8 machine',value ='You are {}% gay :gay_pride_flag:'.format(gay),inline = False)
            await client.say(embed=embed)
        else:
            gay = random.randint(0, 100)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name = 'gay r8 machine',value ='{0} is {1}% gay :gay_pride_flag:'.format(user.name, gay),inline = False)
            await client.say(embed=embed)   
	
@client.command(pass_context=True)
async def gayrate(ctx, user: discord.Member = None):
    if ctx.message.author.bot:
        return
    else:
        if user is None:
            gay = random.randint(0, 100)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name = 'gay r8 machine',value ='You are {}% gay :gay_pride_flag:'.format(gay),inline = False)
            await client.say(embed=embed)
        else:
            gay = random.randint(0, 100)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name = 'gay r8 machine',value ='{0} is {1}% gay :gay_pride_flag:'.format(user.name, gay),inline = False)
            await client.say(embed=embed)        	
        
@client.command(pass_context=True)
async def roll(ctx):
    if ctx.message.author.bot:
        return
    else:
        dice = random.randint(1, 6)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=f"**__Rolling a Die__**", description=f"**You Just Rolled {dice}** :game_die:", colour = discord.Colour((r << 16) + (g << 8) +b))
        await client.say(embed=embed)

@client.command(pass_context = True)
async def whois(ctx, user: discord.Member=None):
    if user is None:
      await client.say('Please tag a user to get user information. Example- ``ad!whois @user``')
    if ctx.message.author.bot:
      return
    else:
      r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
      embed = discord.Embed(title="{}'s info".format(user.name), description="Here is the detail of that user.", color = discord.Color((r << 16) + (g << 8) + b))
      embed.add_field(name="__Name__", value=user.mention, inline=False)
      embed.add_field(name="__USER ID__", value=user.id, inline=False)
      embed.add_field(name="__Status__", value=user.status, inline=False)
      embed.add_field(name="__Highest role__", value=user.top_role)
      embed.add_field(name="__Color__", value=user.color)
      embed.add_field(name="__Playing__", value=user.game)
      embed.add_field(name="__Nickname__", value=user.nick)
      embed.add_field(name="__Joined__", value=user.joined_at.strftime("%d %b %Y %H:%M"))
      embed.add_field(name="__Created__", value=user.created_at.strftime("%d %b %Y %H:%M"))
      embed.set_thumbnail(url=user.avatar_url)
      await client.say(embed=embed)

@client.command(pass_context=True)
async def serverlist(ctx):
    if ctx.message.author.id == '519122918773620747':
        servers = '\n'.join([i.name for i in client.servers]).strip('\n')
        await client.say('**I am currently active on these servers:**\n ```bf\n{}```'.format(servers))
    else:
        await client.say('This command is for bot owner only.')

@client.command(pass_context=True)
async def ownerinfo(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title=f"**My Owner:**", description=f"I was created by <@519122918773620747> :yum:\nOwner's Guild:- https://invite.gg/alistorm", colour = discord.Colour((r << 16) + (g << 8) +b))
    await client.say(embed=embed)    

@client.command(pass_context=True)
async def miniavatar(ctx, user:discord.Member=None):
    if user is None:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name='User Avatar')
        embed.set_thumbnail(url = ctx.message.author.avatar_url)
        await client.send_message(ctx.message.channel, embed=embed)
    else:
       r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
       embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
       embed.set_author(name='User Avatar')
       embed.set_thumbnail(url = user.avatar_url)
       await client.send_message(ctx.message.channel, embed=embed)
	
@client.command(pass_context=True)
async def yt(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://cdn.vox-cdn.com/thumbor/3PGCC3bHmmo9uSN2MJ83zpqIO5o=/0x14:800x547/1200x800/filters:focal(0x14:800x547)/cdn.vox-cdn.com/assets/3124217/new_youtube_logo.jpg")
    embed.add_field(name = '__**YOUTUBE SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed) 

@client.command(pass_context=True)
async def google(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://www.google.com/search?client=firefox-b-d&q={new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3aOiSVQZeEAe4X4lGbdB2Ic9GQs4EsRqTRiqosv212C9f2ZNP")
    embed.add_field(name = '__**GOOGLE SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)       

@client.command(pass_context=True)
async def twitter(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://twitter.com/search?q={new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGmcZbAePkZ9sc65W1udbUGR8908H8jA_AfaIdRGeauYt-HYA2")
    embed.add_field(name = '__**TWITTER SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)   

@client.command(pass_context=True)
async def twitch(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://twitch.tv/{new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://images-eu.ssl-images-amazon.com/images/I/312EjBsxqzL.png")
    embed.add_field(name = '__**TWITCH SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)   

@client.command(pass_context=True)
async def instagram(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://www.instagram.com/{new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://image.freepik.com/free-vector/instagram-icon_1057-2227.jpg")
    embed.add_field(name = '__**INSTAGRAM SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)  

@client.command(pass_context=True)
async def github(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://github.com/{new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://camo.githubusercontent.com/7710b43d0476b6f6d4b4b2865e35c108f69991f3/68747470733a2f2f7777772e69636f6e66696e6465722e636f6d2f646174612f69636f6e732f6f637469636f6e732f313032342f6d61726b2d6769746875622d3235362e706e67")
    embed.add_field(name = '__**GITHUB SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)  

@client.command(pass_context=True)
async def dbl(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://discordbots.org/bot/{new_message}"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://discordbots.org/images/dblnew.png")
    embed.add_field(name = '__**DISCORD BOT VOTING LINK**__',value=url,inline = False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def dblvote(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://discordbots.org/bot/{new_message}/vote"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://discordbots.org/images/dblnew.png")
    embed.add_field(name = '__**DISCORD BOT VOTING LINK**__',value=url,inline = False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def binvite(ctx, *, message: str):
    new_message = message.replace(" ", "+")
    url = f"https://discordapp.com/oauth2/authorize?client_id={new_message}&scope=bot&permissions=8"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "https://fiverr-res.cloudinary.com/images/t_main1,q_auto,f_auto/gigs/107575377/original/34ca93755e2c88b7a11f7399344e5a64d24308cd/make-a-custom-discord-bot-for-you.jpg")
    embed.add_field(name = '__**DISCORD BOT INVITE LINK**__',value=url,inline = False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def amazon(ctx, *, message: str):
    new_message = message.replace(" ", "%20")
    url = f"https://www.amazon.com/s?k={new_message}&ref=nb_sb_noss"
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_thumbnail(url = "http://www.vmastoryboard.com/wp-content/uploads/2014/08/Amazon-Logo_Feature.jpg")
    embed.add_field(name = '__**AMAZON SEARCH LINK**__',value=url,inline = False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def emoji(ctx, *, message: str):
    new_message = message.replace(" ", "_")
    url = f":{new_message}:"
    await client.say(url)

@client.command(pass_context=True)
async def prefix(ctx):
    if ctx.message.author.bot:
        return
    else:    
        await client.say('**__My Prefixes are as follows:-__** \n``` ad! \n AD! \n Or When Mentioned.```')

@client.command(pass_context = True)
async def avatar(ctx, user: discord.Member=None):
    if user is None:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=f'❯Discord Avatar Machine', description='**__Avatar of {0}:__**'.format(ctx.message.author), color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        embed.set_image(url = ctx.message.author.avatar_url)
        await client.say(embed=embed)
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=f'❯Avatar Machine', description="**__Avatar of {0}:__**".format(user), color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        embed.set_image(url = user.avatar_url)
        await client.say(embed=embed)  

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, userName: discord.User=None,*, message:str=None): 
    if userName is None:
      await client.say('Please tag a person to warn user. Example- **ad!warn @user <reason>**')
      return
    if message is None:
        await client.say('Please provide a reason to warn user. Example- **ad!warn @user <reason>**')
        return
    if ctx.message.author.bot:
        return
    else:	
        await client.say("***:white_check_mark: Alright! {0} Has Been Warned for {1}.*** ".format(userName,message))
        for channel in userName.server.channels:
            if channel.name == '〚📑〛server-logs':
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_thumbnail(url=userName.avatar_url)
                embed.add_field(name = 'USER WARNED',value ='***A User Was Warned!***',inline = False)
                embed.add_field(name = '__**WARNED USER:**__',value ='**{}**'.format(userName),inline = False)
                embed.add_field(name = '__**WARNED USER ID:**__',value ='**{}**'.format(userName.id),inline = False)
                embed.add_field(name = '__**WARNED BY:**__',value ='**{}**'.format(ctx.message.author),inline = False)
                embed.add_field(name = '__**REASON:**__',value ='**{}**'.format(message),inline = False)
                embed.add_field(name = '__**WARNED IN:**__',value ='{}'.format(ctx.message.channel.mention),inline = False)
                embed.timestamp = datetime.datetime.utcnow()
                await client.send_message(channel, embed=embed)
                await client.send_message(userName, "You have been warned in **{0}** for **{1}**".format(ctx.message.server, message))

@client.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member=None, *, nickname=None):
    member = user.name
    if user is None:
      await client.say('Please tag a person to change nickname. Example- `` ad!setnick @user <new nickname>``')
      return
    else:
      await client.change_nickname(user, nickname)
      await client.delete_message(ctx.message)
      await client.say('Nickname was successfully changed.')

@client.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_nicknames=True)     
async def resetnick(ctx, user: discord.Member=None):
    member = user.name
    if user is None:
      await client.say('Please tag a person to reset nickname. Example- ``ad!resetnick @user``')
      return
    else:
      nick = user.name
      await client.change_nickname(user, nick)
      await client.delete_message(ctx.message)
      await client.say('Nickname reset was successful.')

@client.command(pass_context = True)
async def channellock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await client.say("{0} Just Locked {1}.".format(ctx.message.author, ctx.message.channel))
    else:
        if ctx.message.author.server_permissions.manage_channels == False:
            await client.say('**You do not have `Manage Channels` permission to use this command.**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("{0} Just Locked {1}.".format(ctx.message.author, channelname))

@client.command(pass_context = True)
async def superlock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=False)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await client.say("{0} Just Locked {1}.".format(ctx.message.author, ctx.message.channel))
    else:
        if ctx.message.author.server_permissions.manage_channels == False:
            await client.say('**You do not have `Manage Channels` permission to use this command.**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("{0} Just Locked {1}.".format(ctx.message.author, channelname))	

@client.command(pass_context = True)
async def channelunlock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=None, read_messages=True)
    if not channelname:
        if ctx.message.author.server_permissions.manage_channels == False:
            await client.say('**You do not have `Manage Channels` permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(ctx.message.channel, role, overwrite)
            await client.say("{0} Unlocked {1}.".format(ctx.message.author, ctx.message.channel))
    else:
        if ctx.message.author.server_permissions.manage_channels == False:
            await client.say('**You do not have `Manage Channels` permission to use this command**')
            return
        else:
            role = discord.utils.get(ctx.message.server.roles, name='@everyone')
            await client.edit_channel_permissions(channelname, role, overwrite)
            await client.say("{0} Unlocked {1}".format(ctx.message.author, channelname))

@client.command(pass_context = True)
@commands.has_permissions(manage_messages = True)
async def purge(ctx, number: int):
  purge = await client.purge_from(ctx.message.channel, limit = number+1)
  await client.say('Purged {0} messages for you.'.format(number))
  for channel in ctx.message.author.server.channels:
        if channel.name == '〚📑〛server-logs':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_author(name='Purge Command Used')
            embed.add_field(name = '__Commander:__ **{0}**'.format(ctx.message.author),value ='__Commander ID:__ **{}**'.format(ctx.message.author.id),inline = False)
            embed.add_field(name = '__Channel:__',value ='{}'.format(ctx.message.channel.mention),inline = False)
            await client.send_message(channel, embed=embed)

@client.command(pass_context = True)
async def ban(ctx, userName: discord.User):
    if ctx.message.author.server_permissions.ban_members:
        await client.ban(userName)
        embed=discord.Embed(title="**User Banned Successfully!**", description="**The User {0} was successfully Banned By {1}!**".format(userName, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
        for channel in ctx.message.server.channels:
          if channel.name == '〚📑〛server-logs':
              embed=discord.Embed(title="User banned!", description="**{0}** was banned by **{1}**!".format(userName, ctx.message.author), color=0x38761D)
              embed.set_thumbnail(url=userName.avatar_url)
              await client.send_message(channel, embed=embed)
              await client.send_message(userName, 'You Were Banned From {0}'.format(ctx.message.server))
    else:
        embed=discord.Embed(title="Command declined!", description="Sorry! You don't have permission to use this command.", color=0x38761D)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def kick(ctx, userName: discord.User):
    if ctx.message.author.server_permissions.kick_members:
        await client.kick(userName)
        embed=discord.Embed(title="**User kicked Successfully!**", description="**The User {0} was successfully kicked By {1}!**".format(userName, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
        for channel in ctx.message.server.channels:
          if channel.name == '〚📑〛server-logs':
              embed=discord.Embed(title="User Kicked!", description="**{0}** was kicked by **{1}**!".format(userName, ctx.message.author), color=0x38761D)
              embed.set_thumbnail(url=userName.avatar_url)
              await client.send_message(channel, embed=embed)
              await client.send_message(userName, 'You Were Kicked From {0}'.format(ctx.message.server))
    else:
        embed=discord.Embed(title="Command declined!", description="Sorry! You don't have permission to use this command.", color=0x38761D)
        await client.say(embed=embed)
	
@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
async def unban(ctx, identification:str):
    user = await client.get_user_info(identification)
    await client.unban(ctx.message.server, user)
    try:
        await client.say(f'`{user}` has been unbanned from the server.')
        for channel in ctx.message.server.channels:
          if channel.name == '〚📑〛server-logs':
              embed=discord.Embed(title="User unbanned!", description="**{0}** was unbanned by **{1}**!".format(user, ctx.message.author), color=0x38761D)
              embed.set_thumbnail(url=user.avatar_url)
              await client.send_message(channel, embed=embed)
              await client.send_message(user, 'You were unbanned from {0}'.format(ctx.message.server))
    except:
        await client.say(f'Unable to unban `{user}`')
        pass 	
	
@client.command(pass_context=True)
async def highlight(ctx,*, message:str=None):	
    if message is None:
        await client.say('```No Messages Were Found!```')
    else:
        await client.say('```{}```'.format(message))

@client.command(pass_context=True)
async def counterstrike(ctx,*, message:str=None):	
    if message is None:
        await client.say('```css\nNo Messages Were Found!```')
    else:
        await client.say('```css\n{}```'.format(message))	

@client.command(pass_context=True)
async def bold(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('**{}**'.format(message))	

@client.command(pass_context=True)
async def strikethrough(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('~~{}~~'.format(message))		

@client.command(pass_context=True)
async def underline(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('__{}__'.format(message))		

@client.command(pass_context=True)
async def italic(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('*{}*'.format(message))		

@client.command(pass_context=True)
async def bolditalic(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('***{}***'.format(message))	

@client.command(pass_context=True)
async def bolditalicunderline(ctx,*, message:str=None):	
    if message is None:
        await client.say('**No Messages Were Found!**')
    else:
        await client.say('***__{}__***'.format(message))		
	
@client.command(pass_context = True)
async def mute(ctx, member: discord.Member=None, mutetime=None):
    if ctx.message.author.server_permissions.administrator:
        if discord.utils.get(member.server.roles, name="Muted") is None:
            await client.create_role(member.server, name="Muted", permissions=discord.Permissions.none())
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            role = discord.utils.get(member.server.roles, name='Muted')
            await client.add_roles(member, role)
            await client.say(':white_check_mark: **Alright! {0} Was Muted!**'.format(member.name))
        else:
            role = discord.utils.get(member.server.roles, name='Muted')
            await client.add_roles(member, role)
            await client.say(':white_check_mark: **Alright! {0} Was Muted!**'.format(member.name))
            for channel in member.server.channels:
                if channel.name == '〚📑〛server-logs':
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name = 'USER MUTED',value ='***A user was Muted in this server.!***',inline = False)
                    embed.add_field(name = '__**MUTED USER:**__',value ='**{}**'.format(member.name),inline = False)
                    embed.add_field(name = '__**MUTED USER ID:**__',value ='**{}**'.format(member.id),inline = False)
                    embed.add_field(name = '__**MODERATOR:**__',value ='**{}**'.format(ctx.message.author),inline = False)
                    embed.add_field(name = '__**MUTED FROM:**__',value ='{}'.format(ctx.message.channel.mention),inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    await client.send_message(channel, embed=embed)
                    await client.send_message(member, "You are muted in **{0}**".format(ctx.message.server))
    else:
        await client.say('Sorry! You need to have `Administrator` permission to use this command.')

@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member=None, mutetime=None):
    if ctx.message.author.server_permissions.administrator:
            role = discord.utils.get(member.server.roles, name='Muted')
            await client.remove_roles(member, role)
            await client.say(':white_check_mark: **Alright! {0} Was Unmuted!**'.format(member.name))
            for channel in member.server.channels:
                if channel.name == '〚📑〛server-logs':
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name = 'USER UNMUTED',value ='***A user was unmuted in this server.!***',inline = False)
                    embed.add_field(name = '__**UNMUTED USER:**__',value ='**{}**'.format(member.name),inline = False)
                    embed.add_field(name = '__**UNMUTED USER ID:**__',value ='**{}**'.format(member.id),inline = False)
                    embed.add_field(name = '__**MODERATOR:**__',value ='**{}**'.format(ctx.message.author),inline = False)
                    embed.add_field(name = '__**UNMUTED FROM:**__',value ='{}'.format(ctx.message.channel.mention),inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    await client.send_message(channel, embed=embed)
                    await client.send_message(member, "You are muted in **{0}**".format(ctx.message.server))
    else:
        await client.say('Sorry! You need to have `Administrator` permission to use this command.')		   

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def banlist(ctx):
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "Here Is The List of The Banned Idiots Of This Server", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context=True)
async def invites(ctx, user:discord.Member=None):
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        if user is None:
            total_uses=0
            embed=discord.Embed(title='Invites from {}'.format(ctx.message.author.name), color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            invites = await client.invites_from(ctx.message.server)
            for invite in invites:
              if invite.inviter == ctx.message.author:
                  total_uses += invite.uses
                  embed.add_field(name='❯ Invites',value = "https://discord.gg/{}".format(invite.id,inline=False))
                  embed.add_field(name='❯ Invites Used',value=invite.uses,inline=False)
                  embed.add_field(name='❯ Channel',value=invite.channel.mention,inline=False)
                  embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.add_field(name='❯ Total Uses',value=total_uses,inline=False)
            await client.say(embed=embed)
        else:
            total_uses=0
            embed=discord.Embed(title='Invites from {}'.format(user.name), color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_thumbnail(url=user.avatar_url)
            invites = await client.invites_from(ctx.message.server)
            for invite in invites:
              if invite.inviter == user:
                  total_uses += invite.uses
                  embed.add_field(name='❯ Invite Link',value = "https://discord.gg/{}".format(invite.id,inline=False))
                  embed.add_field(name='❯ Uses',value=invite.uses,inline=False)
                  embed.add_field(name='❯ Channel',value=invite.channel.mention,inline=False)
                  embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.add_field(name='❯ Total Uses',value=total_uses,inline=False)
            await client.say(embed=embed)

@client.command(pass_context=True)
async def www(ctx, user1: discord.Member, user2: discord.Member = None):
    if ctx.message.author.bot:
        return
    else:
        user1url = user1.avatar_url
        user2url = user2.avatar_url  
        url = (f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1=%s&user2=%s" % (user1url, user2url,))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)

@client.command(pass_context=True)
async def distract(ctx, user1: discord.Member, user2: discord.Member = None):
    if ctx.message.author.bot:
        return
    else:
        if user2 is None:
            user2 = ctx.message.author

        if user1.avatar:
            user1url = "https://cdn.discordapp.com/avatars/%s/%s.png" % (user1.id, user1.avatar,)
        else:
            user1url = "https://cdn.discordapp.com/embed/avatars/1.png"
        if user2.avatar:
            user2url = "https://cdn.discordapp.com/avatars/%s/%s.png" % (user2.id, user2.avatar,)
        else:
            user2url = "https://cdn.discordapp.com/embed/avatars/1.png"
            
        url = (f"https://nekobot.xyz/api/imagegen?type=ship&user1=%s&user2=%s" % (user1url, user2url,))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)               

@client.command(pass_context=True)
async def lolice(ctx):
    if ctx.message.author.bot:
        return
    else:
        usrl = ctx.message.author.avatar_url  
        url = (f"https://nekobot.xyz/api/imagegen?type=lolice&url=%s" % (usrl))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await client.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await client.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['👍', '👎']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']
        
        question.split('"')
        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=question, description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        react_message = await client.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await client.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await client.edit_message(react_message, embed=embed)
        await client.delete_message(ctx.message)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.name == '〚🇻〛verification':
        if reaction.emoji == "🇻":
            role = discord.utils.get(reaction.message.server.roles, name="Verified")
            await client.add_roles(user, role)
            await client.send_message(user, f'You Were Given `Verified` role in **{reaction.message.server}**')
    else:
        return        
	
@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.name == '〚🇻〛verification':
        if reaction.emoji == "🇻":
            role = discord.utils.get(user.server.roles, name="Verified")
            await client.remove_roles(user, role)
            await client.send_message(user, f'You Were Removed From `Verified` Role in **{reaction.message.server}**')
    else:
        return        

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setverification(ctx):
    author = ctx.message.author
    server = ctx.message.server
    everyone_perms = discord.PermissionOverwrite(send_messages=False,read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    await client.create_channel(server, '〚🇻〛verification',everyone)
    for channel in author.server.channels:
        if channel.name == '〚🇻〛verification':
            react_message = await client.send_message(channel, 'Please React With "🇻" To Verify Yourself.')
            reaction = '🇻'
            await client.add_reaction(react_message, reaction)
	
@client.command(pass_context=True)
async def embed(ctx, *args):
    argstr = " ".join(args)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    text = argstr
    color = discord.Color((r << 16) + (g << 8) + b)
    await client.send_message(ctx.message.channel, embed=Embed(color = color, description=text))
    await client.delete_message(ctx.message)		

@client.command(pass_context=True)
async def clyde(ctx, *, text:str):
    if ctx.message.author.bot:
        return
    else: 
        url = f"https://nekobot.xyz/api/imagegen?type=clyde&text=%s" % text
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "Clyde said :/ {}".format(text)
                await client.say(embed=embed)
@client.command(pass_context=True)
async def blur(ctx, member: discord.Member=None):
    if not member:
        usrl = ctx.message.author.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=blurpify&image=%s" % usrl
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)
    else:
        usrl = member.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=blurpify&image=%s" % usrl
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)
		
@client.command(pass_context=True)
async def phub(ctx, user:discord.Member, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = (f"https://nekobot.xyz/api/imagegen?type=phcomment"
                    f"&image={user.avatar_url}"
                    f"&text={txt}&username={user.name}")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed) 		

@client.command(pass_context=True)
async def virus(ctx,user: discord.Member=None,*,hack=None):
    nome = ctx.message.author
    if not hack:
        hack = 'arxytoped'
    else:
        hack = hack.replace(' ','_')
    channel = ctx.message.channel
    x = await client.send_message(channel, '``[▓▓▓                    ] / {}-discordvirus.exe Packing files.``'.format(hack))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-discordvirus.exe is Initializing to download.``'.format(hack))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-discordvirus.exe is Downloading..``'.format(hack))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-discordvirus.exe Downloaded.``'.format(hack))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Starting {}-virus.exe``'.format(hack))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Injecting virus in``{0}s system ``.   |``'.format(user.mention))
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Virus Successfully Injected To`` {0}s `system`'.format(user.mention))
    await client.delete_message(ctx.message)
    await client.delete_message(x)
        
    if user:
        await client.say('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
        await client.send_message(user,'**Alert!**\n``Your System Contains Virus. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
    else:
        await client.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
        await client.send_message(name,'**Alert!**\n``Your System Contains virus. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))		
		
@client.command(pass_context=True)
async def hack(ctx,user: discord.Member=None,*,hack=None):
    nome = ctx.message.author
    if not hack:
        hack = 'discord hacker'
    else:
        hack = hack.replace(' ','_')
    channel = ctx.message.channel
    x = await client.send_message(channel, '``[▓▓▓                    ] / {}-Starting Hacking Tool.``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-Started Hacking Tool..``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {0}-Starting to crack discord password of`` {1}``...``'.format(hack, user.mention))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {0}-Starting to crack nitro key of`` {1}``.``'.format(hack, user.mention))
    await asyncio.sleep(1)
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Hacking Done {}- Downloading Files``'.format(hack))
    await asyncio.sleep(1)
    x = await client.edit_message(x,'``Files Downloaded... -``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``Showing Results....\``')
    await asyncio.sleep(0.5)
    x = await client.edit_message(x,'``check your DMs``')
    await client.delete_message(x)
    await client.delete_message(ctx.message)
        
    if user:
        await client.send_message(nome, 'I Found This:-\n Nitro Key- https://discord.gift/UllHB2ejgpB40AjB \n Discord password- imdiscord123 \n '.format(hack,user.name))
        await client.send_message(user,'**Alert!**\n``You may have been hacked. Change your passwords now.``'.format(hack))
    else:
        await client.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
        await client.send_message(name,'**Alert!**\n``You hacked yourself. Change your password right now¯\_(ツ)_/¯.``'.format(hack))		
		
@client.command(pass_context=True)
async def threats(ctx, user: discord.Member):
    if ctx.message.author.bot:
        return
    else:
        img = user.avatar_url  
        url = (f"https://nekobot.xyz/api/imagegen?type=threats&url=%s" % img)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed)

@client.command(pass_context=True)
async def shitpost(ctx):
    if ctx.message.author.bot:
        return
    else:
        url = (f"https://www.reddit.com/r/copypasta/hot.json?sort=hot")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                data = random.choice(res["data"]["children"])["data"]
                em = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b), title=data["title"], description=data["selftext"], url=data["url"])
                em.set_footer(text="Neko API|nekobot.xyz")
                await client.say(embed=em)		
		
@client.command(pass_context=True)
async def iphonex(ctx, user: discord.Member):
    if ctx.message.author.bot:
        return
    else:
        img = user.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=iphonex&url={img}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "{} Took Selfie in iphonex".format(user.name)
                await client.say(embed=embed)		

@client.command(pass_context=True)
async def bodypillow(ctx, user: discord.Member=None):
    if ctx.message.author.bot:
        return
    else:
        if user is None:
            img = ctx.message.author.avatar_url  
            url = (f"https://nekobot.xyz/api/imagegen?type=bodypillow&url=%s" % img)
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_image(url=res['message'])
                    embed.title = "What??? {} Is A Bodypillow?".format(ctx.message.author.name)
                    await client.say(embed=embed) 
        else:
            img = user.avatar_url  
            url = (f"https://nekobot.xyz/api/imagegen?type=bodypillow&url=%s" % img)
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_image(url=res['message'])
                    embed.title = "What??? {} Is A Bodypillow?".format(user.name)
                    await client.say(embed=embed)	

@client.command(pass_context=True)
async def changemymind(ctx, *, text: str):
    if ctx.message.author.bot:
        return
    else: 
        url = f"https://nekobot.xyz/api/imagegen?type=changemymind&text=%s" % text
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                await client.say(embed=embed) 			

@client.command(pass_context=True)
async def fact(ctx, *, text: str):
    if ctx.message.author.bot:
        return
    else: 
        if text is None:
          await client.say('Please enter text')
        else:
            url = f"https://nekobot.xyz/api/imagegen?type=fact&text={text}"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_image(url=res['message'])
                    await client.say(embed=embed) 		

@client.command(pass_context=True)
async def fight(ctx, user1: discord.Member, user2: discord.Member = None):
    if ctx.message.author.bot:
        return
    else: 
        if user2 == None:
            user2 = ctx.message.author

        win = random.choice([user1, user2])

        if win == user1:
            lose = user2
        else:
            lose = user1

        await client.say("%s Kicked %s Outta Discord!" % (win.mention, lose.mention,))

@client.command(pass_context=True)
async def kannagen(ctx, *, text:str):
    if ctx.message.author.bot:
        return
    else: 
        if text is None:
          url = f"https://nekobot.xyz/api/imagegen?type=kannagen&text=KANNAGEN"
          async with aiohttp.ClientSession() as cs:
              async with cs.get(url) as r:
                  res = await r.json()
                  r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                  embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                  embed.set_image(url=res['message'])
                  await client.say(embed=embed) 
        else:
            url = f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                    embed.set_image(url=res['message'])
                    await client.say(embed=embed)  

@client.command(pass_context=True)
async def dong(ctx, *, user: discord.Member):
    if ctx.message.author.bot:
        return
    else: 
        state = random.getstate()
        random.seed(user.id)
        dong = "8{}D".format("=" * random.randint(0, 30))
        random.setstate(state)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title="Dong Size Of {0}".format(user.name), description="**SIZE: \n**" + dong, color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url=user.avatar_url)
        await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def deepfry(ctx, user: discord.Member = None):
    if ctx.message.author.bot:
        return
    else:
        img = user.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=deepfry&image=%s" % img
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "{} was deepfried.".format(user.name)
                await client.say(embed=embed)


		
@client.command(pass_context=True)
async def trash(ctx, user: discord.Member):
    if ctx.message.author.bot:
        return
    else:
        vrl = user.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=trash&url=%s" % (vrl,)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "{} is Trash".format(user.name)
                await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def captcha(ctx, user: discord.Member):
    if ctx.message.author.bot:
        return
    else:
        vrl = user.avatar_url  
        url = f"https://nekobot.xyz/api/imagegen?type=captcha&url=%s&username=%s" % (vrl, user.name,) 
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "Select All Images With {}".format(user.name)
                await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "{} just twitted: {}".format(usernamename, txt)
                await client.say(embed=embed)

@client.command(pass_context=True)
async def tseriestweet(ctx, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = f"https://nekobot.xyz/api/imagegen?type=tweet&username=tseries&text={txt}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "T-Series just twitted: {}".format(txt)
                await client.say(embed=embed)	

@client.command(pass_context=True)
async def aerotweet(ctx, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = f"https://nekobot.xyz/api/imagegen?type=tweet&username=aerodynamicbot&text={txt}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "I just twitted: {}".format(txt)
                await client.say(embed=embed)		

@client.command(pass_context=True)
async def pewdstweet(ctx, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = f"https://nekobot.xyz/api/imagegen?type=tweet&username=pewdiepie&text={txt}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "PewDiePie just twitted: {}".format(txt)
                await client.say(embed=embed)		
		
@client.command(pass_context=True)
async def trumptweet(ctx, *, txt:str):
    if ctx.message.author.bot:
        return
    else:    
        url = f"https://nekobot.xyz/api/imagegen?type=trumptweet&username=Trump&text={txt}"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                res = await r.json()
                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
                embed.set_image(url=res['message'])
                embed.title = "Trump just twitted: {}".format(txt)
                await client.say(embed=embed)  

@client.command(pass_context = True)
async def troll(ctx):
    if ctx.message.author.bot:
        return
    else:
        ml = ["👍 256", "👍 1K", "👍 6.5K", "👍 203K", "👍 1M", "👍 97K", "👍 500K", "👍 100K", "👍 6K"]
        co = ["💬 126", "💬 19K", "💬 3K", "💬 70K", "💬 1M", "💬 10M", "💬 2.3K", "💬 917", "💬 67K"]
        title = ["What do you call someone with no nose? Nobody knows.", "Dad, can you put my shoes on? I don't think they'll fit me.", "Toasters were the first form of pop-up notifications.", "What do you get hanging from Apple trees? Sore arms.", "Atheism is a non-prophet organisation.", "Why do mathematicians hate the U.S.? Because it's indivisible.", "Can February march? No, but April may.", "What does a female snake use for support? A co-Bra!", "What do you call a boomerang that won't come back? A stick.", "Why did the coffee file a police report? It got mugged.", "Why did the girl smear peanut butter on the road? To go with the traffic jam.", "A bartender broke up with her boyfriend, but he kept asking her for another shot.", "How many apples grow on a tree? All of them!"]
        like = random.choice(ml)
        comment = random.choice(co)
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title='**__❯ DISCORD MEME__**', description=random.choice(title), color = discord.Color((r << 16) + (g << 8) + b))
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.reddit.com/r/me_irl/random") as r:
                data = await r.json()
                embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.set_footer(text=f'{random.choice(ml)} | {random.choice(co)}', icon_url=f'{ctx.message.author.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                await client.say(embed=embed)    		

@client.command(pass_context = True, aliases=["8ball"])
async def eightball(ctx, *, question:str=None):
    if question is None:
        await client.say(":x: Please Use It Like This:- `ad!8ball Your_question`")
        return
    else:
        choices = [
        "What the hell?",
        "I Think; Yes!",
        "Maybe.",
        "I Don't Know.",
        "You shouldn't think that.",
        "Sounds like cancer.",
        "Why do you need that",
        "Hell No!",
        "Prolly.",
        "Hell Yeah.",
        "Hmm... Yeah!",
        "Prolly Not.",
        "Might Be.",
        "If You Think That, You Are A Gay.",
        "What A Cruel World!",
        "Oof!",
        "Am I A Joke To You?",
        "That question looks fucking bad.",
        "Thats Gay!",
        "One Day...",
        "Agreed..",
        "Of Course",
        "Exactly",
        "LMAO, is that a joke?",
        "LMFAO! Is that even a question?",
        "Are you kidding?",
        "You baka; Thats true.",
        "Nope.",
        "You Are Right.",
        "100% True.",
        "Yeah!",
        "Umm.. No!",
        ]

    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name = "🎱 8-BALL QUESTION 🎱")
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.add_field(name = ":basketball_player: **__Player__**", value = "{}".format(ctx.message.author.mention), inline=False)
    embed.add_field(name = ":question: **__Question__**", value = "{}".format(question), inline=False)
    embed.add_field(name = ":8ball:**__Answer__**", value = "{}".format(random.choice(choices)), inline=False)
    embed.set_footer(text=f'{client.user.display_name}.xyz', icon_url=f'{client.user.avatar_url}')
    embed.timestamp = datetime.datetime.utcnow()
    await client.say(embed=embed)		
		
@client.command(pass_context = True)
async def qna(ctx, *, msg:str):
    if msg is None:
      await client.say('```I cant get message for QNA```')
      return
    else:
      choices = ["Maybe", "I Don't Think So", "I Think So", "What A Loser", "Really Naga? If You Think So, Go And Eat Your Own Poop."]
      r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
      embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
      embed.set_thumbnail(url=ctx.message.author.avatar_url)
      embed.add_field(name = '__**DISCORD QNA**__',value = 'QNA CHANNEL: ``{}``'.format(ctx.message.channel),inline = False)
      embed.add_field(name = '__**QUESTION**__',value=msg,inline = False)
      embed.add_field(name = '__**ANSWER BY BOT**__',value=random.choice(choices),inline = False)
      embed.set_footer(text=f'ASKED BY: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
      embed.timestamp = datetime.datetime.utcnow()
      await client.say(embed=embed) 
      await client.delete_message(ctx.message) 		
		
@client.command(pass_context = True)
async def time(ctx):
    if ctx.message.author.bot:
        return
    else:    
        timestamp = datetime.datetime.utcnow()
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.add_field(name = '__**The Time Is:**__',value ='```{}```'.format(timestamp),inline = False)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def help(ctx):
    if ctx.message.author.bot:
        return
    else:    
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name='HELP CENTER OF ROYBOT')
        embed.add_field(name = '__**❯ Blogspot Help:**__',value ='https://sites.google.com/view/roybothelp/home',inline = False)
        embed.timestamp = datetime.datetime.utcnow()
        await client.say(embed=embed)

@client.command(pass_context=True)
async def invite(ctx):
    if ctx.message.author.bot:
        return
    else: 
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/552818527623708673/581373006127824896/photo.jpg")
        embed.add_field(name = '__**INVITE LINK:**__',value ='https://discordapp.com/api/oauth2/authorize?client_id=550655965733847043&permissions=8&scope=bot',inline = False)  
        await client.say(embed=embed)

@client.command(pass_context=True)      
async def serverinfo(ctx):

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: 
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Server Owner__', value = str(server.owner) + "\n **__Owner's ID__**  " + server.owner.id);
    join.add_field(name = '__Server ID__', value = str(server.id))
    join.add_field(name = '__Members Count Of This Server__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels in this server__', value = str(channelz));
    join.add_field(name = '__Available Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Server was Created on: %s'%time);

    return await client.say(embed = join);

@client.command(pass_context = True)
async def setupserver(ctx):
    author = ctx.message.author
    server = ctx.message.server
    if author.bot:
        return
    if author.server_permissions.administrator:
        mod_perms = discord.Permissions(manage_messages=True, kick_members=True, manage_nicknames =True,mute_members=True)
        admin_perms = discord.Permissions(administrator=True)
        muted_perms = discord.Permissions(send_message=False)
        await client.delete_message(ctx.message)
        await client.create_role(author.server, name="Owner", permissions=admin_perms)
        await client.create_role(author.server, name="Head Admin", permissions=admin_perms)
        await client.create_role(author.server, name="Admins", permissions=mod_perms)
        await client.create_role(author.server, name="YouTubers")
        await client.create_role(author.server, name="Moderators", permissions=mod_perms)
        await client.create_role(author.server, name="Muted")
        await client.create_role(author.server, name="Friends")
        await client.create_role(author.server, name="Members")
        await client.create_role(author.server, name="Bots", permissions=admin_perms)
        await client.say('Roles were created successfully!')
    
        everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
        everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
        user_perms = discord.PermissionOverwrite(read_messages=True)
        user = discord.ChannelPermissions(target=server.default_role, overwrite=user_perms)
        private_perms = discord.PermissionOverwrite(read_messages=False)
        private = discord.ChannelPermissions(target=server.default_role, overwrite=private_perms)
        await client.create_channel(server, 'welcome-bye',everyone)
        await client.create_channel(server, 'rules',everyone)
        await client.create_channel(server, 'announcements',everyone)
        await client.create_channel(server, 'info',everyone)
        await client.create_channel(server, 'giveaways',everyone)
        await client.create_channel(server, 'uploads',everyone)
        await client.create_channel(server, 'chit-chat',user)
        await client.create_channel(server, 'foreign-chat',user)
        await client.create_channel(server, 'bot-commands',user)
        await client.create_channel(server, 'media-chat',user)
        await client.create_channel(server, 'memes',user)
        await client.create_channel(server, 'self-promotion',user)
        await client.create_channel(server, 'music-zone',user)
        await client.create_channel(server, 'VOICE-1', type=discord.ChannelType.voice)
        await client.create_channel(server, 'VOICE-2', type=discord.ChannelType.voice)
        await client.create_channel(server, 'chat-for-staffs',private)
        await client.create_channel(server, 'server-logs',private)
        await client.say('I have done setup!')
    else:
        await client.say("Sorry! You Don't Have Permissions To Use This Command. ")    

@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name == 'hoi-bye':
            embed = discord.Embed(title=f' :tada: Welcome **{member.name}** to **{member.server.name}** :tada:', description='Do not forget to check rules and never try to break any one of them. Thank You.', color = 0x36393E)
            embed.add_field(name='__Total Members__', value='Now We Have **{}** Members.'.format(str(member.server.member_count)), inline=False)
            embed.set_thumbnail(url=member.avatar_url) 
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            await asyncio.sleep(0.2)
            await client.send_message(channel, embed=embed)

@client.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == 'welcome-bye-royster':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f' :confounded: **{member.name}** just left **{member.server.name}** :confounded:', description='Bye bye! We will miss you.', color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name='__User left__', value='**Hope You Will Come Back Again.**', inline=True)
            embed.add_field(name='__Total Members__', value='Now We Have **{}** Members.'.format(str(member.server.member_count)), inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            await client.send_message(channel, embed=embed)             

@client.command(pass_context=True)
async def jointest(ctx):
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'welcome-bye-royster':
            embed = discord.Embed(title=f' :tada: Welcome **{member.name}** to **{member.server.name}** :tada:', description='Do not forget to check rules and never try to break any one of them. Thank You.', color = 0x36393E)
            embed.add_field(name='__Total Members__', value='Now We Have **{}** Members.'.format(str(member.server.member_count)), inline=False)
            embed.set_thumbnail(url=member.avatar_url) 
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            await asyncio.sleep(0.2)
            await client.send_message(channel, embed=embed)

@client.command(pass_context=True)
async def leavetest(ctx):
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'welcome-bye-royster':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f' :confounded: **{member.name}** just left **{member.server.name}** :confounded:', description='Bye bye! We will miss you.', color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name='__User left__', value='**Hope You Will Come Back Again.**', inline=True)
            embed.add_field(name='__Your Join position Was__', value='**{}**'.format(str(member.server.member_count)), inline=True)
            embed.add_field(name='__Total Members__', value='Now We Have **{}** Members.'.format(str(member.server.member_count)), inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            await client.send_message(channel, embed=embed) 
		
@client.command(pass_context = True)
async def setwelcomer(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command.**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'welcome-bye-royster',everyone)
      await client.say('welcome-bye channel has been created.')

@client.command(pass_context = True)
async def setsuggestions(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command.**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'suggestions',everyone)
      await client.say('suggestions channel has been created.')

@client.command(pass_context = True)
async def setlogging(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command.**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=False)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'server-logs',everyone)
      await client.say('Logging channel has been created.')

@client.command(pass_context = True)
async def setchat(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command.**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=True, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, '〚👾〛bot-chat',everyone)
      await client.say('Bot Chat channel has been created.')

@client.command(pass_context = True)
async def suggest(ctx, *, msg: str=None):
    if ctx.message.author.bot:
      return
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'suggestions':
          if msg is None:
            await client.say('**INVALID COMMANDS WERE GIVEN. USE THIS COMMAND LIKE** `r!suggest <suggestions>`')
          else:
              r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
              embed=discord.Embed(title="**__SUGGESTIONS BY {0}__**".format(member), description="{}".format(msg), color = discord.Color((r << 16) + (g << 8) + b))
              embed.set_thumbnail(url=ctx.message.author.avatar_url)
              await client.send_message(channel, embed=embed)
              await client.delete_message(ctx.message)
              await client.say(':white_check_mark: ***Your Suggestions Were Sent.***')

@client.command(pass_context = True)
async def promote(ctx, *, msg: str=None):
    if ctx.message.author.bot:
      return
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'self-promotion':
          if msg is None:
            await client.say('**INVALID COMMANDS WERE GIVEN. USE THIS COMMAND LIKE** `r!promote <link>`')
          else:
              r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
              embed=discord.Embed(title="**__{0} Shared a link__**".format(member), description="{}".format(msg), color = discord.Color((r << 16) + (g << 8) + b))
              embed.set_thumbnail(url=ctx.message.author.avatar_url)
              await client.send_message(channel, embed=embed)
              await client.delete_message(ctx.message)
              await client.say(':white_check_mark: ***Your Links Were Sent.***')		
		
@client.command(pass_context = True)
async def suggestreply(ctx, *, msg: str=None):
    if ctx.message.author.bot:
      return
    member = ctx.message.author
    for channel in member.server.channels:
        if channel.name == 'suggestions':
          if msg is None:
            await client.say('**INVALID COMMANDS WERE GIVEN. USE THIS COMMAND LIKE** `r!suggestreply <suggestions>`')
          else:
              if member.server_permissions.kick_members:
                  r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                  embed=discord.Embed(title="**__REPLY TO THE SUGGESTIONS BY {0}__**".format(member), description="{}".format(msg), color = discord.Color((r << 16) + (g << 8) + b))
                  embed.set_thumbnail(url=ctx.message.author.avatar_url)
                  await client.send_message(channel, embed=embed)
                  await client.delete_message(ctx.message)
              else:
                  await client.say('You Dont Have Permissions To Use This Command.')               

client.run('NTg1ODEyMTQzNDQ2Njg3NzY1.XPjv6g.4gEqQKkBkK4BpJFthsiY1a7RAmg')