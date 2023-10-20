# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import asyncio
import os
import json


with open("./config.json", encoding = "utf-8") as config:
    configData = json.load(config)

__version__ = configData["Version"]
TOKEN = configData["Token"]
GuildId = configData["GuildId"]
OwnerId = configData["WonerId"]


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

bot = commands.Bot(command_prefix = commands.when_mentioned_or("$"), owner_id = OwnerId, activity = ac, status = discord.Status.dnd, intents = intents)




@bot.event
async def on_ready():
    await bot.tree.sync(guild = discord.Object(id = GuildId))
    await bot.wait_until_ready()
    print(f"Logged in as {bot.user}(ID: {bot.user.id}) | Version: {__version__}")
bot.remove_command("help")

@bot.tree.command(name = "sync", description = "update commands", guild = discord.Object(id = GuildId))
async def sync(interaction: discord.Interaction, text: str = None, server_id: str = None):
    if interaction.user.id == bot.owner_id:
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
    if interaction.user.id == bot.owner_id:
        try:
            await bot.load_extension(f"cogs.{extension}")
            await interaction.response.send_message(f"loaded `{extension}` done.", ephemeral = True)
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(f"Not found`cog.{extension}`", ephemeral = True)
    else:
        await interaction.response.send_message("**no premission**", ephemeral = True)

@bot.tree.command(name = "unload", description = "unload cog file", guild = discord.Object(id = GuildId))
async def unload(interaction: discord.Interaction, extension: str):
    if interaction.user.id == bot.owner_id:
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
    if interaction.user.id == bot.owner_id:
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
            print(f'Loaded {filename[:-3]}.')
    print('Done.')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())



