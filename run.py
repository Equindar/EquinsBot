# --- imports
import discord
import sys, traceback
from discord.ext import commands
from cfg.identity import *         # AUTHKEY file from http://discordapp.com

# --- init
# list of extensions [./ext]
extensions = ['ext.system',
              'ext.errors',
              'ext.codegen',
              'ext.dev',
              'ext.Northgard.init'
             ]
# initialize the bot
bot = commands.Bot(command_prefix='!', description="A universal Discord Bot by Equindar")
bot.log = 521619613708976135

# --- main
if __name__ == '__main__':
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(f"Failed to load extension {ext}.", file=sys.stderr)
            traceback.print_exc()
        print(f"[System] Bot Extension: {ext} loaded.")

# bot event on_ready()
@bot.event
async def on_ready():
    print("[Bot] Logging in...")
    print(f"[Bot] Identity: {bot.user.name} [ID: {bot.user.id}]")

# run the bot
bot.run(AUTHKEY, bot=True, reconnect=True)
