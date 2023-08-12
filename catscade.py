import string
import time
import datetime
import calendar
import disnake
import os
import copy
import math
import random
import asyncio 
import aiohttp
from disnake import Webhook
from enum import Enum
from disnake.activity import Activity, Game
from disnake.app_commands import Option, OptionChoice
from disnake.enums import ButtonStyle, OptionType, Status
from disnake.ext import commands

bot = commands.InteractionBot(intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Logged in as")   
    print(bot.user.name)
    print(bot.user.id) 
    print("----------------")
    act = Game(name="Anarchic")  
    await bot.change_presence(activity=act, status=Status.do_not_disturb)

links = {}
relaynick = {}
id = 0

# class Relay:
#     def __init__(self, input, player, name, link, hook) -> None:
#         self.input:disnake.TextChannel = input
#         self.id = len(links) + 1
#         self.player:disnake.Member = player
#         self.name:str = name
#         self.avatar:str = link
#         self.webhook:Webhook = hook
#         links[player.id] = self

# @bot.slash_command(
#     name="create_relay",
#     description="Create a relay from this channel",
#     options=[
#             Option("output", "output", OptionType.channel, True),
#             Option("player", "player", OptionType.user, True),
#             Option("name", "name", OptionType.string, True),
#             Option("image_link", "image_link", OptionType.string, True)
#         ]
# )
# async def relay(inter, output:disnake.TextChannel, player, name, image_link):
#     hook = await output.create_webhook(name=str(len(links) + 1))
#     Relay(inter.channel, player, name, image_link, hook)
    
#     await inter.response.send_message("Relay created!", ephemeral=True)

# @bot.slash_command(
#     name="view_relays",
#     description="View the current relays",
# )
# async def view_relays(inter):
#     embed = disnake.Embed(title="Relays")
#     for i in links.values():
#         i:Relay
#         embed.add_field(f"ID `{i.id}` | `{i.name}` for {i.player.name}", f"<:hertaspin:1138251556991537233> from {i.input.mention} to {i.webhook.channel.mention}")
    
#     await inter.response.send_message(embed=embed)

# @bot.event
# async def on_message(message:disnake.Message):
#     if (message.author.id in links.keys()):
#         relay:Relay = links[message.author.id]
#         if (message.channel.id == relay.input.id):
#             await relay.webhook.send(content=message.content, username=relay.name, avatar_url=relay.avatar)

## HOST COMMANDS

admin = [487045257981067289]
hosts = []
canTrollbox = []

@bot.slash_command(
name="config",
description="Change the permissions for a member",
options=[
    Option("player", "player", OptionType.user, True),
    Option("permission", "permission", OptionType.string, True)
]
)

async def config(inter, player, permission):
    if inter.author.id not in admin:
        await inter.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    if permission == "host":
        if player.id not in hosts:
            hosts.append(player.id)
            await inter.response.send_message(f"**{player.name}** is now a host!", ephemeral=True)
        else:
            hosts.remove(player.id)
            await inter.response.send_message(f"**{player.name}** is no longer a host!", ephemeral=True)
    elif permission == "trollbox":
        if player.id not in canTrollbox:
            canTrollbox.append(player.id)
            await inter.response.send_message(f"**{player.name}** can now use **Trollbox**!", ephemeral=True)
        else:
            canTrollbox.remove(player.id)
            await inter.response.send_message(f"**{player.name}** can no longer use **Trollbox**!", ephemeral=True)
@config.autocomplete("permission")
async def autoCompleteConfig(inter, string:str):
    permissions = ["host", "trollbox"]
    return permissions

@bot.slash_command( 
name="set_channel",
description="Set a channel to a specific type",
    options=[
            Option("type", "type", OptionType.string, True)
        ]
)

async def set_channel(inter, type):
    global gameChannels
    global hostChannel

    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    if type == "game":
        gameChannels = inter.channel
        await inter.response.send_message("Channel has been setup as the game channel!", ephemeral=True)
    elif type == "host":
        hostChannel = inter.channel
        await inter.response.send_message("Channel has been setup as the host channel!", ephemeral=True)
            
@set_channel.autocomplete("type")
async def autoCompleteSet_Channel(inter, string:str):
    channels = ["game", "host"]
    return channels

## RELAYS

class NewRelay:
    def __init__(self, input, player, name, link, output, hex) -> None:
        global id
        self.input:disnake.TextChannel = input
        self.id = id + 1
        self.player:disnake.Member = player
        self.name:str = name
        self.link:str = link
        self.output = output
        self.hex = hex
        links[player.id] = self
        relaynick[name] = player.id

@bot.slash_command(name="relay")
async def relaybase(inter):
    pass

@relaybase.sub_command(
    name="create",
    description="Create a relay from this channel",
    options=[
            Option("output", "output", OptionType.channel, True),
            Option("player", "player", OptionType.user, True),
            Option("name", "name", OptionType.string, True),
            Option("image_link", "image_link", OptionType.string, False),
            Option("hex", "hexcode", OptionType.string, False)
        ]
)

async def relay(inter, output:disnake.TextChannel, player, name, image_link="https://images-ext-2.discordapp.net/external/ADJGsnNezWhz-eLsDFuJOu3tr0UAZS4cExlEqz4wbQM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/915388341736857630/4dec84b546872bf25f1fdcd7136cd934.png?width=664&height=664", hex="ffffff"):
    global id
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    if player.id == 915388341736857630:
        await inter.response.send_message("You cannot create a relay with catscade.", ephemeral=True)
    else:
        NewRelay(inter.channel, player, name, image_link, output, hex)
        id += 1
        await inter.response.send_message("Relay created!", ephemeral=True)

@relaybase.sub_command(
    name="delete",
    description="Delete a relay",
    options=[
        Option("id", "id", OptionType.integer, True)
    ]
)
async def del_relay(inter, id):
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    idsToDel = []
    for i in links.values():
        i:NewRelay
        if i.id == id:
            idsToDel.append(i.player.id)

    del links[i.player.id]
    
    await inter.response.send_message("Relay deleted!", ephemeral=True)

@relaybase.sub_command(
    name="view",
    description="View the current relays",
)
async def view_relays(inter):
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    if inter.channel != hostChannel:
        await inter.response.send_message(f"This command can only be used in a host channel!", ephemeral=True)
        return
    embed = disnake.Embed(title="Relays", colour=0xdefeff)
    for i in links.values():
        i:NewRelay
        embed.add_field(f"ID `{i.id}` | `{i.name}` for {i.player.name}", f"<a:hertaspin:1138251556991537233> from {i.input.mention} to {i.output.mention}", inline=False)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ADJGsnNezWhz-eLsDFuJOu3tr0UAZS4cExlEqz4wbQM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/915388341736857630/4dec84b546872bf25f1fdcd7136cd934.png?width=664&height=664")
    await inter.response.send_message(embed=embed)

@bot.event
async def on_message(message:disnake.Message):
    if (message.author.id in links.keys()):
        relay:NewRelay = links[message.author.id]
        if (message.channel.id == relay.input.id):
            try:
                int(relay.hex, 16)
            except:
                relay.hex == "ffffff"
            date = datetime.datetime.utcnow()
            utc_time = calendar.timegm(date.utctimetuple())
            embed = disnake.Embed(title=f"`{relay.name}` | <t:{utc_time}:t>", colour=int(relay.hex, 16), description=f"{message.content}")
            try:
                embed.set_thumbnail(url=relay.link)
                await relay.output.send(embed=embed)
            except:
                embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ADJGsnNezWhz-eLsDFuJOu3tr0UAZS4cExlEqz4wbQM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/915388341736857630/4dec84b546872bf25f1fdcd7136cd934.png?width=664&height=664")
                await relay.output.send(embed=embed)

## WHISPERS

whispers = {}
whisperers = {}
whisperChannels = {}
gameChannels = "channel"
hostChannel = "channel"
whisperID = 0

class Whisper:
    def __init__(self, channel, player, nickname) -> None:
        self.channel = channel
        self.player:disnake.Member = player
        self.nickname:str = nickname
        whispers[player.id] = self
        whisperers[nickname] = player
        whisperChannels[nickname] = channel
        self.id = whisperID + 1

@bot.slash_command( 
name="whisper",
description="Whisper to a player",
    options=[
            Option("player", "player", OptionType.string, True),
            Option("message", "message", OptionType.string, True)
        ]
)

async def whisper(inter, player:str, message):
    global gameChannels
    if inter.author.id not in whispers.keys():
        await inter.response.send_message("You do not have a registered relay.", ephemeral=True)
        return
    whisper:Whisper = whispers[inter.author.id]
    if (player not in whisperers.keys()):
        await inter.response.send_message(f"{player} does not have a registered relay.", ephemeral=True)
        return
    if gameChannels == "channel":
        await inter.response.send_message("Whispers have not been set up.", ephemeral=True)
        return
    receiverchannel = whisperChannels[player]
    await gameChannels.send(f"**{whisper.nickname} <:whisper:922242257715879946>** is whispering to **{player}**")
    await whisper.channel.send(f"**{whisper.nickname} to {player} <:whisper:922242257715879946>:** {message}")
    await receiverchannel.send(f"**{whisper.nickname} to {player} <:whisper:922242257715879946>:** {message}")
    await inter.response.send_message(f"You sent the whisper <:whisper:922242257715879946>", ephemeral=True)
    if hostChannel != "channel":
        await hostChannel.send(f"**{whisper.nickname} to {player} <:whisper:922242257715879946>:** {message}")

@whisper.autocomplete("player")
async def autocompletewhisper(inter, string:str):
    canBeWhispered = []
    for i in whisperers.keys():
        if (string in i):
            canBeWhispered.append(i)
    canBeWhispered.sort()
    return canBeWhispered

@bot.slash_command( 
name="add_whisper",
description="Create a whisper channel",
    options=[
            Option("player", "player", OptionType.user, True),
            Option("nickname", "nickname", OptionType.string, True)
        ]
)

async def add_whisper(inter, player, nickname="catscade"):
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    global whisperID
    if (nickname == "catscade"):
        nickname = player.name
    if nickname in whisperers.keys():
        await inter.response.send_message("Another player is already registered with that nickname.", ephemeral=True)
        return
    if inter.channel in whisperChannels.keys():
        await inter.response.send_message("Another player is already registered in the current channel.", ephemeral=True)
        return
    Whisper(inter.channel, player, nickname)
    whisperID += 1
    await inter.response.send_message("Whisper channel added!", ephemeral=True)

@bot.slash_command( 
name="del_whisper",
description="Delete a whisper channel",
    options=[
        Option("id", "id", OptionType.integer, True)
    ]
)

async def del_whisper(inter, id):
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    idsToDel = []
    for i in whispers.values():
        i:Whisper
        if i.id == id:
            idsToDel.append(i.player.id)

    del whispers[i.player.id]
    await inter.response.send_message("Whisper channel deleted!", ephemeral=True)


@bot.slash_command( 
name="view_whispers",
description="View the current whisper relays"
)

async def view_whispers(inter):
    if inter.author.id not in hosts:
        await inter.response.send_message(f"You aren't a host!", ephemeral=True)
        return
    if inter.channel != hostChannel:
        await inter.response.send_message(f"This command can only be used in a host channel!", ephemeral=True)
        return
    embed = disnake.Embed(title="Whispers", colour=0xdefeff)
    for i in whispers.values():
        i:Whisper
        embed.add_field(f"ID `{i.id}` | `{i.player.name}` as {i.nickname}", f"<a:hertaspin:1138251556991537233> from {i.channel.mention}", inline=False)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ADJGsnNezWhz-eLsDFuJOu3tr0UAZS4cExlEqz4wbQM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/915388341736857630/4dec84b546872bf25f1fdcd7136cd934.png?width=664&height=664")
    await inter.response.send_message(embed=embed)

## TROLLBOX
@bot.slash_command( 
name="trollbox",
description="Say something as another player",
    options=[
            Option("player", "player", OptionType.string, True),
            Option("message", "message", OptionType.string, True)
        ]
)

async def trollbox(inter, player, message):
    if inter.author.id not in canTrollbox:
        await inter.response.send_message(f"You cannot Trollbox. Please DM the host if there is an issue.", ephemeral=True)
    relay:NewRelay = links[relaynick[player]]
    try:
        int(relay.hex, 16)
    except:
        relay.hex == "ffffff"
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    embed = disnake.Embed(title=f"`{relay.name}` | <t:{utc_time}:t>", colour=int(relay.hex, 16), description=f"{message}")
    try:
        embed.set_thumbnail(url=relay.link)
        await relay.output.send(embed=embed)
    except:
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ADJGsnNezWhz-eLsDFuJOu3tr0UAZS4cExlEqz4wbQM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/915388341736857630/4dec84b546872bf25f1fdcd7136cd934.png?width=664&height=664")
        await relay.output.send(embed=embed)    
    await inter.response.send_message(f"You used the *Troll Box* on **{player}**", ephemeral=True)
    if hostChannel != "channel":
        await hostChannel.send(f"**{inter.author.name}** used **Trollbox** on **{player} ({relay.player})**: {message}")


@trollbox.autocomplete("player")
async def autoCompleteTrollbox(inter, string:str):
    canBeTrollboxed = []
    for i in relaynick.keys():
        if (string in i):
            canBeTrollboxed.append(i)
    canBeTrollboxed.sort()
    return canBeTrollboxed

bot.run(os.environ["DISCORD_TOKEN"])
