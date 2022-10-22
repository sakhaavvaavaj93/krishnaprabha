
import os
import sys
import asyncio
import subprocess
from time import sleep
from threading import Thread
from signal import SIGINT
from pyrogram import Client, filters, idle
from config import Config
from utils import mp, USERNAME, FFMPEG_PROCESSES
from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw.types import BotCommand, BotCommandScopeDefault
from user import USER
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant

ADMINS=Config.ADMINS


bot = Client(
    "RadioPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins.bot")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()
        try:
            await USER.join_chat("DC_Kurukshethra")
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            print(e)
            pass

def stop_and_restart():
    bot.stop()
    os.system("git pull")
    sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()
print("\n\nDC Player Bot Started, Join @DC_Kurukshethra!")
bot.send(
    SetBotCommands(
        scope=BotCommandScopeDefault(),
        lang_code="en",
        commands=[
            BotCommand(
                command="start",
                description="Start The Bot"
            ),
            BotCommand(
                command="help",
                description="Show Help Message"
            ),
            BotCommand(
                command="play",
                description="Play Music From YouTube"
            ),
            BotCommand(
                command="song",
                description="Download Music As Audio"
            ),
            BotCommand(
                command="skip",
                description="Skip The Current Music"
            ),
            BotCommand(
                command="pause",
                description="Pause The Current Music"
            ),
            BotCommand(
                command="resume",
                description="Resume The Paused Music"
            ),
            BotCommand(
                command="radio",
                description="Start Radio / Live Stream"
            ),
            BotCommand(
                command="current",
                description="Show Current Playing Song"
            ),
            BotCommand(
                command="playlist",
                description="Show The Current Playlist"
            ),
            BotCommand(
                command="join",
                description="Join To The Voice Chat"
            ),
            BotCommand(
                command="leave",
                description="Leave From The Voice Chat"
            ),
            BotCommand(
                command="stop",
                description="Stop Playing The Music"
            ),
            BotCommand(
                command="stopradio",
                description="Stop Radio / Live Stream"
            ),
            BotCommand(
                command="replay",
                description="Replay From The Begining"
            ),
            BotCommand(
                command="clean",
                description="Clean Unused RAW PCM Files"
            ),
            BotCommand(
                command="mute",
                description="Mute Userbot In Voice Chat"
            ),
            BotCommand(
                command="unmute",
                description="Unmute Userbot In Voice Chat"
            ),
            BotCommand(
                command="volume",
                description="Change The Voice Chat Volume"
            ),
            BotCommand(
                command="restart",
                description="Update & Restart Bot (Owner Only)"
            ),
            BotCommand(
                command="setvar",
                description="Set / Change Configs Var (For Heroku)"
            )
        ]
    )
)

@bot.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(ADMINS)
async def restart(_, message: Message):
    k=await message.reply_text("🔄 **Checking ...**")
    await asyncio.sleep(3)
    if Config.HEROKU_APP:
        await k.edit("🔄 **Heroku Detected, \nRestarting Your App...**")
        Config.HEROKU_APP.restart()
    else:
        await k.edit("🔄 **Restarting, Please Wait...**")
        process = FFMPEG_PROCESSES.get
        if process:
            try:
                process.send_signal(SIGINT)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(e)
                pass
            FFMPEG_PROCESSES = ""
        Thread(
            target=stop_and_restart()
            ).start()
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @DC_LOGS For Update!**")
        await k.reply_to_message.delete()
    except:
        pass

idle()
print("\n\nDC Player Bot Stopped, Join @DC_Kurukshethra!")
bot.stop()
