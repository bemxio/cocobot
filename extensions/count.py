from discord.ext import commands, tasks
from discord import Embed, Colour

from datetime import datetime
import assets.config as cf
import json, os.path

class MessageCounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = []
        
        if not os.path.exists("assets/count_msg.json"):
            self.fetch.start()
        
        with open("assets/count_msg.json", "r") as file:
            self.messages = json.load(file)
        
        if not self.messages:
            self.fetch.start()
        
    @tasks.loop(days=1)
    async def fetch(self):
        await self.bot.wait_until_ready()
        
        for channel_id in cf.count_channels:
            channel = self.bot.get_channel(channel_id)

            async for message in channel.history(limit=None):
                self.messages.append({"author": message.author.id, "content": message.content})
        
        with open("assets/count_msg.json", "w") as file:
            json.dump(self.messages, file, indent=4)

        self.fetch.stop()
    
    @commands.command()
    async def count(self, ctx, *, text):
        messages = {}

        for message in self.messages:
            if text.lower() in message["content"].lower():
                if not messages.get(message["author"]):
                    messages[message["author"]] = 0

                messages[message["author"]] += 1
        
        messages = dict(sorted(messages.items(), key=lambda x: x[1], reverse=True))
        embed = Embed(
            title=f"Top #10 users who've typed '{text}':", 
            colour=Colour.orange()
        )

        index = 0
        for user_id, count in messages.items():
            user = self.bot.get_user(user_id)

            embed.add_field(
                name=f"#{index + 1} - {str(user)}",
                value=f"**{count}** uses",
            )

            if index == 9:
                break
            
            index += 1
        
        await ctx.message.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.messages.append({"author": message.author.id, "content": message.content})
    
def setup(bot):
    bot.add_cog(MessageCounting(bot))