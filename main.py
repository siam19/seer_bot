import discord
import os
from discord.ext import commands
from discord.ext.commands import Context
from discord.channel import TextChannel
from discord.message import Message
import requests

from utlis import send_transcript


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())



@bot.event
async def on_message(message: Message):
    if message.attachments is not None:
        for attachment in message.attachments:
            if attachment.filename.startswith("seavoice-bot-transcript"):
                try:
                    print("found new transcript!")
                    res = await send_transcript(attachment.url)
                    channel= bot.get_channel(message.channel.id)
                    await channel.send(res)
                except requests.RequestException as e:
                    print(f"Error downloading or reading the file: {e}")

            



@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(os.getenv("DISCORD_TOKEN"))

