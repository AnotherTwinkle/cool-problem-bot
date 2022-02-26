import discord
import tasks

class CoolBot(discord.Client):
    def __init__(self, intents):
        super(CoolBot, self).__init__(intents = intents)
        self.task = tasks.BotTasks(self)

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

        # These are in self.task.send_problem()
        # if message.channel.id == channelID:
        #     await message.add_reaction("<:pepeyessign:889089415174058026>")
        #     await message.add_reaction("<:pepenosign:889089399072108584>")

        # New commands
        if message.content.startswith('-cool'):
            # Arguments "channel", "command", "reactions" for flexibilty
            await self.task.send_problem(message, "cool-problems", "-cool", ["<:pepeyessign:889089415174058026>", "<:pepenosign:889089399072108584>"])
    
        # Same can be done for marathon problems
        elif message.content.startswith('-marathon'):
            await self.task.send_problem(message, "marathon-problems", '-marathon', ["<:plus_one:896423100953022504>", "<:minus_one:938471992976367676>"])

        # Help command
        elif message.content.startswith("-help"):
            with open("help_msg.txt", encoding = "utf8") as f:
                await message.channel.send(f.read())