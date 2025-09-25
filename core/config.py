import os
import discord

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

GUILD_ID = discord.Object(id=1192230487280848896)
DEVS = [901913992434434128]

VERSION = "0.1.0"