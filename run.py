#!/usr/bin/python

# --- imports
import discord
import asyncio
import time

#from settings.config import *
#from modules.System import System


#sys = System()

def main():
    print("initializing...")
    bla
    # --- init
    client = discord.Client()

    # register Event handler
    @client.event
    async def on_ready():
        print("initializing Bot...")
        print("Logged in as %s (%s)" % (client.user.name, client.user.id))

    @client.event
    async def on_message(msg):
        # do not communicate with yourself
        if message.author == client.user:
            return

        if msg.content == "cookie":
            await bot.send_message(message_channel, ":cookie:")
    # login the Bot

    client.run("NTA4OTgxMDA0NzE1OTUwMDkw.DtWlVA.ZnidWJa5diqjYwBX2WVx91HPnfw")

if __name__ == "__main__":
    main()
