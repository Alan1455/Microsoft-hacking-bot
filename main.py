# -*- coding: utf-8 -*-

# discord 
import discord
from discord import app_commands
from discord.ext import commands, tasks

# system class
from antispam import AntiSpamHandler
from antispam.enums import Library
from pprint import pprint
from typing import List
from discord import utils
from typing import Any
import time
import asyncio
import random
import datetime
import os
import sys
import string
import math

# miscellaneous 
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import requests
import uuid
import openai
import json


with open("./config.json", encoding = "utf-8") as config:
    configData = json.load(config)

__version__ = configData["Version"]
TOKEN = configData["Token"]
GuildId = configData["GuildId"]

with open("./members.json", encoding = "utf-8") as members:
    membersData = json.load(members)

owners: dict = membersData["Owner"]
admins: dict  = membersData["Admins"]


colorama_init()
class color:
    HEADER = Fore.MAGENTA
    OKBLUE = Fore.BLUE
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    ENDC = Style.RESET_ALL

MISSING: Any = utils._MissingSentinel()




ac = discord.Streaming(name = "", url = "")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.emojis = True
intents.presences = True
intents.dm_reactions = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.moderation = True
intents.integrations = True
intents.voice_states = True
intents.guilds = True
intents.auto_moderation = True
intents.webhooks = True
intents.invites = True

bot = commands.Bot(command_prefix = commands.when_mentioned_or("$"), owner_id = 868108080850812939, activity = ac, status = discord.Status.dnd, intents = intents)

bot._handlers = AntiSpamHandler(bot, library = Library.DPY)




@bot.event
async def on_ready():
    await bot.tree.sync(guild = discord.Object(id = GuildId))
    await bot.wait_until_ready()
    print(f"{Fore.RED}Logged in as {color.WARNING}{bot.user} {color.HEADER}(ID: {bot.user.id}){color.ENDC} | {color.OKGREEN}Version: {__version__}{color.ENDC}")
bot.remove_command("help")

@bot.tree.command(name = "sync", description = "update commands", guild = discord.Object(id = GuildId))
async def sync(interaction: discord.Interaction, text: str = None, server_id: str = None):
    if interaction.user.id in list(owners.values()):
        if text == "this":
            sy = await bot.tree.sync(guild = discord.Object(id = GuildId))
            await interaction.response.send_message(f"Synced {len(sy)} commands.", ephemeral = True)
            return

        if text == "all":
            sy = await bot.tree.sync()
            await interaction.response.send_message(f"Synced {len(sy)} commands.", ephemeral = True)
            return

        if text == None and server_id:
            sy = await bot.tree.sync(guild = discord.Object(id = int(server_id)))
            await interaction.response.send_message(f"Synced {len(sy)} commands.", ephemeral = True)
            return

        await interaction.response.send_message("Sorry, something wrong!")
    else:
        await interaction.response.send_message("**no premission**", ephemeral = True)


@bot.tree.command(name = "load", description = "load cog file", guild = discord.Object(id = GuildId))
async def load(interaction: discord.Interaction, extension: str):
    if interaction.user.id in list(admins.values()) or interaction.user.id in list(owners.values()):
        try:
            await bot.load_extension(f"cogs.{extension}")
            await interaction.response.send_message(f"loaded `{extension}` done.", ephemeral = True)
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(f"Not found`cog.{extension}`", ephemeral = True)
    else:
        await interaction.response.send_message("**no premission**", ephemeral = True)

@bot.tree.command(name = "unload", description = "unload cog file", guild = discord.Object(id = GuildId))
async def unload(interaction: discord.Interaction, extension: str):
    if interaction.user.id in list(admins.values()) or interaction.user.id in list(owners.values()):
        try:
            await interaction.guild.voice_client.disconnect()
        except:
            pass

        try:
            await bot.unload_extension(f"cogs.{extension}")
            await interaction.response.send_message(f"unloaded `{extension}` done.", ephemeral = True)
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(f"Not found`cog.{extension}`", ephemeral = True)
    else:
        await interaction.response.send_message("**no premission**", ephemeral = True)

@bot.tree.command(name = "reload", description = "reload cog file", guild = discord.Object(id = GuildId))
async def reload(interaction: discord.Interaction, extension: str):
    if interaction.user.id in list(admins.values()) or interaction.user.id in list(owners.values()):
        try:
            await interaction.guild.voice_client.disconnect()
        except:
            pass

        if extension == "all":
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    await bot.reload_extension(f"cogs.{filename[:-3]}")
            await interaction.response.send_message(f"reloaded `all` done.", ephemeral = True)
        else:
            try:
                await bot.reload_extension(f"cogs.{extension}")
                await interaction.response.send_message(f"reloaded `{extension}` done.", ephemeral = True)
            except commands.errors.ExtensionNotLoaded:
                await interaction.response.send_message(f"Not found`cog.{extension}`", ephemeral = True)
    else:
        await interaction.response.send_message("**no premission**", ephemeral = True)




async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f'Loaded {color.WARNING}{filename[:-3]}{color.ENDC}.')
    print('Done.')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())



