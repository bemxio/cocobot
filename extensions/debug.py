from datetime import datetime
from discord.ext import commands, tasks
from discord import Guild

#from aiofile import async_open
import assets.config as cf

from datetime import datetime
import credentials
import aiohttp
import shutil

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def temperature(self, ctx):
        """
        async with async_open(cf.temperature_file, "r") as f:
            temp = await f.read()
    
        await ctx.send(f"Current CPU temperature: {round(int(temp) / 1000, 1)}°C")
        """
        await ctx.send("Since the bot is hosted on DigitalOcean, `pd temperature` doesn't have much sense now :^)")
    
    @commands.command()
    async def latency(self, ctx):
        await ctx.send(f"Current Discord WebSocket protocol latency: {round(self.bot.latency * 1000)} ms")
        
    @commands.command()
    async def billing(self, ctx):
        if not credentials.digitalocean_api_token:
            return
        
        await ctx.send("getting data from digitalocean, please wait...")

        token = credentials.digitalocean_api_token
        url = "https://api.digitalocean.com/v2/customers/my/balance"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        data = None
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as r:
                    if r.ok:
                        data = await r.json()
        
        if not data:
            return await ctx.message.reply("something happened while taking data from digitalocean and i can't take it, sorry :(")
        
        #print(data)
        
        balance = -(float(data["month_to_date_balance"]))
        hours_left = round(balance / 0.007)
        days_left = round(hours_left / 24, 1)
        
        await ctx.message.reply(
            cf.billing.format(
                balance,
                hours_left,
                days_left
            )
        )
        
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        self.bot.cogs["Chatter"].dump_model.stop() # a dirty oneliner to stop the memory saving task
        self.bot.cogs["Impersonation"].save_webhooks.stop() # and a dirty oneliner to stop the webhook saving task
        
        await ctx.send("shutting down...")
        await self.bot.close()

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_time.start()
        
    @tasks.loop(seconds=1)
    async def check_time(self):
        now = datetime.now()
        if now.minute == 00 and now.second == 00:
            await self.copy_memory()
    
    async def copy_memory(self):
        shutil.copy(cf.path, cf.backup_path)

def setup(bot):
    bot.add_cog(Debug(bot))
    bot.add_cog(Backup(bot))