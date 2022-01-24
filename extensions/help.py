# pylint: disable=import-error
# pylint: disable=no-member
# pylint: disable=report-missing-imports

from discord.ext import commands
from datetime import datetime
import assets.config as cf
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = "all my commands!",
            description = "",
            colour = discord.Colour.orange(),
            timestamp = datetime.now(),
        )
        embed.set_footer(text=f"invoked by {str(ctx.author)}", icon_url=str(ctx.author.avatar_url))

        for command, docs in cf.helpdocs.items():
            embed.description += f"""
            **{command}**
            usage: `{docs["usage"]}`
            {docs["description"]}"""

        await ctx.author.send(embed=embed)
        await ctx.message.reply("check your dms! :)", mention_author=False)
        
    @commands.command()
    async def credits(self, ctx):
        await ctx.message.reply(cf.credits, mention_author=False)

def setup(bot):
    bot.add_cog(Help(bot))