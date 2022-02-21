from bot import CoolBot
from keep_alive import keep_alive
import discord

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    token = os.environ.get('TOKEN')
    bot = CoolBot(intents = discord.Intents.all())
    bot.intents.members = True
    bot.intents.presences = True
    bot.intents.guilds = True
    bot.intents.messages = True
    keep_alive()
    bot.run(token)

if __name__ == '__main__':
    main()
