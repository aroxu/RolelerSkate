import re
import discord
from discord import app_commands
from discord.ext import commands
import requests


class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="mcstat", description="Minecraft 서버 상태를 가져옵니다.")
    @app_commands.describe(address="서버 주소")
    async def _mc_server_status(self, interaction: discord.Interaction, address: str) -> None:
        await interaction.response.defer(thinking=True)

        try:
            api_endpoint = "https://api.mcstatus.io/v2/status/java"
            api_url = f"{api_endpoint}/{address}"
            response = requests.get(api_url)
            jsonData = None

            if response.ok:
                jsonData = response.json()
            else:
                return await interaction.followup.send(f"서버 상태를 가져오는 도중 오류가 발생하였습니다: {response.status_code}", ephemeral=False)

            if jsonData["online"] == False:
                embed = discord.Embed(
                    title=f"{address} 서버 상태", description=f"서버가 오프라인입니다.", color=0xff0000)

                return await interaction.followup.send(embed=embed, ephemeral=False)

            motd = jsonData["motd"]["clean"]
            version = jsonData["version"]["name_clean"]
            players = jsonData["players"]["online"]
            max_players = jsonData["players"]["max"]

            embed = discord.Embed(
                title=f"{address} 서버 상태", description=f"서버가 온라인입니다.", color=0x00ff00)
            embed.add_field(
                name="MOTD", value=f">>> {motd}", inline=False)
            embed.add_field(name="버전", value=version, inline=False)
            embed.add_field(
                name="플레이어", value=f"{players}/{max_players}", inline=False)

            return await interaction.followup.send(embed=embed, ephemeral=False)
        except Exception as e:
            return await interaction.followup.send(f"서버 상태를 가져오는 도중 오류가 발생하였습니다: {e}", ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Minecraft(bot))
