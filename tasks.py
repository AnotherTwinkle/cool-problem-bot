import discord
import discord.utils
from flagparser import *
import asyncio

class BotTasks():
    def __init__(self, bot):
        self.client = bot
    
    def embed_problem(self, message, command):
        # Remove the command keyword from the beginning of the string
        txt = message.content[len(command) + 1:]
        # Parse arguments
        datas = parse_flags(txt, ["-title", "-problem", "-hint", "-source", "-difficulty"])
        if datas["-title"] == None: datas["-title"] = "Problem"

        # Set up embed
        embed = discord.Embed(title = datas["-title"] if datas["-title"] != None else "Random Cool Problem",
            colour = 0x0066CB)

        # Show message author in embed
        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
        # Add image to embed if any attachment is given
        if len(message.attachments) > 0:
            embed.set_image(url = message.attachments[0].url)
        else:
            return -1
        # Add fields according to given flags
        if datas["-hint"] != None:
            embed.add_field(name = "Hint", value = datas["-hint"], inline = False)
        if datas["-source"] != None:
            embed.add_field(name = "Source", value = datas["-source"], inline = False)
        if datas["-difficulty"] != None:
            embed.add_field(name = "Difficulty", value = datas["-difficulty"])
        if command == "-cool":
            embed.set_footer(text = "Is the problem cool 🆒?")

        return embed

    async def send_problem(self, message, channel_name, command, reactions = None):
        to_channel = discord.utils.get(message.channel.guild.channels, name = channel_name)
        if to_channel == None or message.channel.name == "tst-bots-and-spam":
            to_channel = message.channel
        try:
            embed = self.embed_problem(message, command)
            if embed == -1:
                await message.channel.send("❗\nNo attachment found!")
                return
            problem_msg = await to_channel.send(embed = embed)
            await problem_msg.add_reaction("❌")
            ok_msg = await message.channel.send("✅\nSent the problem to {0.mention}\nYou can edit the message to resend or delete the problem by reacting ❌ in 1 minute".format(to_channel))
        except:
            await message.channel.send("❗\nInvalid command syntex. Type `-help` for more.")
            return

        # ------- Functionalities before PR -------
        # if command == "-cool":
        if reactions != None:
            for reaction in reactions:
                try:
                    await problem_msg.add_reaction(reaction)
                except:
                    pass

        # --------------------------------------------------------------------------------------------------

        # Check if the message is edited or ❌ readtion is added
        def check_react(reaction, user):
            return reaction.message == problem_msg and user == message.author and str(reaction.emoji) == '❌'
        def check_edit(before, after):
            return before == message

        # Wait 1 minutes for the user
        done, pending = await asyncio.wait([
                            self.client.loop.create_task(self.client.wait_for('message_edit', timeout = 60.0, check = check_edit)),
                            self.client.loop.create_task(self.client.wait_for('reaction_add', timeout = 60.0, check = check_react))
                        ], return_when=asyncio.FIRST_COMPLETED)

        for future in done:
            future.exception()
        for future in pending:
            future.cancel()

        try:
            stuff = done.pop().result()

            # If reacted "❌"
            if type(stuff[0]) == discord.Reaction:
                await problem_msg.delete()
                await message.add_reaction('⏹️')
            # If edited, delete and resend
            else:
                await problem_msg.delete()
                await ok_msg.delete()
                # edited_message = stuff[1]
                await self.send_problem(stuff[1], channel_name, command, reactions = reactions)
            
        except asyncio.TimeoutError:
            await message.add_reaction('⏹️')
            await problem_msg.clear_reaction('❌')

        # ---------------------------------------------------------------------------------------