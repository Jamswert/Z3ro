import discord
from discord.ext import commands
from discord import app_commands

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_listener(self.on_moderation)
    
    async def on_moderation(self, interaction: discord.Interaction, target: discord.Member, action: str, reason: str, moderator : discord.Member):
        channel = discord.utils.get(interaction.guild.channels, name="moderation-logs")
        embed = discord.Embed(
            title=f"Z3ro Detected Moderation",
            description=f"Z3ro has detected a {action} action has been executed.",
            color=0x7289da
        )
        embed.add_field(
            name=f"{action}",
            value=f"The targetted user id was ({target.id}), name: {target.display_name}",
            inline=False
        )
        embed.add_field(
            name="Reason:",
            value=f"The reason stated by the moderator was: {reason}",
            inline=False
        )
        embed.set_footer(text=f"The moderation was requested by name: [{moderator.name}], id: [{moderator.id}]")

        await channel.send(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))