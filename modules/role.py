import re
import discord
from discord import app_commands
from discord.ext import commands


class Role(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="역할", description="자기 자신에게 커스텀 색상 역할을 부여합니다.")
    @app_commands.describe(color="색상 코드 (ex: #FF0000)")
    async def _setrole(self, interaction: discord.Interaction, color: str) -> None:
        if color.startswith("#"):
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
            if not match:
                embed = discord.Embed(
                    title="올바른 색상 코드를 입력해주세요.", description="예시: #123456 또는 #FFFF00", color=0xff0000)
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            color = color[1:]
        else:
            match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color)
            if not match:
                embed = discord.Embed(
                    title="올바른 색상 코드를 입력해주세요.", description="예시: #123456 또는 #FFFF00", color=0xff0000)
                return await interaction.response.send_message(embed=embed, ephemeral=True)

        for user_role in interaction.user.roles:
            if user_role.name.startswith("RSColor_"):
                await interaction.user.remove_roles(user_role)

        for role in interaction.guild.roles:
            if role.name == f"RSColor_{color}":
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"역할 {role.mention}을(를) 성공적으로 부여하였습니다.", ephemeral=True)
                return
        role = await interaction.guild.create_role(name=f"RSColor_{color}", color=discord.Color(int(color, 16)), hoist=True, mentionable=False)

        role_position = interaction.guild.me.top_role.position - 1
        await role.edit(position=role_position)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"역할 {role.mention}을(를) 성공적으로 부여하였습니다.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Role(bot))
