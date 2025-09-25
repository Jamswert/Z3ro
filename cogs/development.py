import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from core.config import DEVS, VERSION

class Development(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()
    
    development = app_commands.Group(name="development", description="Development Commands.")

    @development.command(name="ping", description="Returns the bot's latency.")
    async def ping(self, interaction : discord.Interaction):
        if interaction.user.id not in DEVS:
            await interaction.response.send_message("🚫 You are not a developer, therefore you can't use this command.", ephemeral=True)
            return
        
        latency_ms = round(self.bot.latency * 1000)

        await interaction.response.send_message(f"{latency_ms}ms - Pong!")
    
    @development.command(name="uptime", description="Returns the uptime of the bot.")
    async def uptime(self, interaction: discord.Interaction):
        if interaction.user.id not in DEVS:
            await interaction.response.send_message("🚫 You are not a developer, therefore you can't use this command.", ephemeral=True)
            return

        delta = datetime.now() - self.start_time
        days, remainder = divmod(delta.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_string = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

        embed = discord.Embed(
            title="Uptime",
            description="The uptime of the bot.",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="Uptime",
            value=uptime_string,
            inline=False
        )
        embed.set_footer(text="The uptime of the bot.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @development.command(name="version", description="Returns the version of the bot.")
    async def version(self, interaction: discord.Interaction):
        if interaction.user.id not in DEVS:
            await interaction.response.send_message("🚫 You are not a developer, therefore you can't use this command.", ephemeral=True)
            return

        await interaction.response.send_message(f"The current version of Z3ro is: Z3ro-{VERSION}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Development(bot))