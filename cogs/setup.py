# Import Required Discord Libary and Import(s).
import discord
from discord.ext import commands
from discord import app_commands

from data.database import add_guild, get_guild

class SetupContainer(discord.ui.Container):
    title = discord.ui.TextDisplay("# Z3ro Setup")
    belowtitle = discord.ui.TextDisplay("Run the following Commands to Adjust your Server Specifc Settings")

    gap = discord.ui.Separator()

    command1 = discord.ui.TextDisplay("## /settings config")

class SetupView(discord.ui.LayoutView):
    container = SetupContainer(accent_color=0x7289da)

class MyContainer(discord.ui.Container):
    text = discord.ui.TextDisplay("# Thank you for adding Z3ro to your Server!")
    text1 = discord.ui.TextDisplay("Click the following button for help with Setup")
    
    action_row = discord.ui.ActionRow()

    @action_row.button(label="Setup")
    async def setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.add_reactions:
            print("Clicked the button.")
            print("Adding guild")
            add_guild(int(interaction.guild.id))
            print("Added guild")
            print(get_guild(interaction.guild.id))
            await interaction.response.send_message(view=SetupView())
            print("Sent setupview")
        else:
            await interaction.response.send_message("You are unable to use this command, please consult an Admin.", ephemeral=True)
        
class WelcomeMessage(discord.ui.LayoutView):
    container = MyContainer(accent_color=0x7289da)

# Class for Setup Cog.
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.system_channel
        if not channel:
            print("⚠️ No system channel found.")
            return

        view = WelcomeMessage()
        await channel.send(view=view)

# Adds Cog to Z3ro Bot Class.
async def setup(bot):
    await bot.add_cog(Setup(bot))