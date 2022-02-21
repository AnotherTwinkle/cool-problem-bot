from bot import CoolBot
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
    bot.run(token)

if __name__ == '__main__':
    main()
