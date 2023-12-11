import asyncio
import datetime
import logging
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import TOKEN
from background import *


class Five(commands.Bot):
    def __init__(self, **kwargs):
        intent = discord.Intents.all()
        super().__init__(command_prefix=TOKEN.prefix,
                         intents=intent)

        self.remove_command("help")

    async def setup_hook(self):
        self.loop.create_task(self.load_all_extensions())
        self.loop.create_task(change_activity(self))

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await asyncio.sleep(1)
        commands = [x.stem for x in Path('modules').glob('*.py')]
        for extension in commands:
            try:
                await self.load_extension(f'modules.{extension}')
                print(f'Successfully loaded {extension}.')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'Failed to load: {error}')
            print('-' * 10)

    async def on_ready(self):
        print('-' * 10)
        self.app_info = await self.application_info()
        print(f'Logged in as {self.user.name}\n'
              f'Discord.py version: {discord.__version__}\n'
              f'Owner: {self.app_info.owner}\n'
              f'Invite Link : https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=268463166')
        print('-' * 10)

    async def on_message(self, msg):
        if msg.author.bot:
            return
        await self.process_commands(msg)

    async def on_guild_join(self, guild):
        print(f'Joined server {guild.name} with {guild.member_count} members!')

    async def on_command_error(self, ctx, reason):
        if isinstance(reason, CommandNotFound):
            return
        print(f'There was an error: {reason}')


async def main():
    logging.basicConfig(level=logging.INFO)
    five = Five(config=TOKEN)
    await five.start(TOKEN.bot_token)

asyncio.run(main())
