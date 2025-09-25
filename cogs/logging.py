import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from data.database import get_guild

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
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.avatar:
            avatar_url = member.avatar.url
        else:
            avatar_url = member.default_avatar.url
        
        welcome_embed = discord.Embed(
            title="New Join",
            description="A member has joined the server.",
            color=discord.Color.green()
            )
        welcome_embed.add_field(
            name=f"Member:",
            value=f"{member.mention}",
            inline=False
        )
        welcome_embed.add_field(
            name=f"Time of Join",
            value=datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
            inline=False
        )
        welcome_embed.set_footer(
            text="User joined the server.",
            icon_url=avatar_url)
        guild_data = get_guild(member.guild.id)
        logging = guild_data["logging_enabled"]
        if logging:
            channel = discord.utils.get(member.guild.text_channels, name="member-logs")
            await channel.send(embed=welcome_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.avatar:
            avatar_url = member.avatar.url
        else:
            avatar_url = member.default_avatar.url
        
        welcome_embed = discord.Embed(
            title="New Leave",
            description="A member has left the server.",
            color=discord.Color.red()
            )
        welcome_embed.add_field(
            name=f"Member:",
            value=f"{member.mention}, Name: {member.display_name}",
            inline=False
        )
        welcome_embed.add_field(
            name=f"Time of Leave",
            value=datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
            inline=False
        )
        welcome_embed.set_footer(
            text="User left the server.",
            icon_url=avatar_url)
        guild_data = get_guild(member.guild.id)
        logging = guild_data["logging_enabled"]
        if logging:
            channel = discord.utils.get(member.guild.text_channels, name="member-logs")
            await channel.send(embed=welcome_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))