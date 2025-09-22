import os
import discord

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

GUILD_ID = discord.Object(id=1373285906315743293)