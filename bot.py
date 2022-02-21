import discord

channelID = 942764372164481094

class CoolBot(discord.Client):
    async def on_connect(self):
        print('[LOGS] Connecting to discord!')

    async def on_ready(self):
         print('[LOGS] Bot is ready!')
         print("""[LOGS] Logged in: {}\n[LOGS] ID: {}\n[LOGS] Number of users: {}""".format(self.user.name, self.user.id, len(set(self.get_all_members()))))
         await self.change_presence(activity=discord.Game(name="Send cool problems in #cool-problems"))

    async def on_resumed(self):
         print("\n[LOGS] Bot has resumed session!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id == channelID:
            await message.add_reaction("<:pepeyessign:889089415174058026>")
            await message.add_reaction("<:pepenosign:889089399072108584>")

