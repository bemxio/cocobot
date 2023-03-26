# pylint: disable=import-error
# pylint: disable=no-member

from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands, tasks
from discord import User, Embed, Colour
from discord import utils, AllowedMentions

from assets.modules import markov, meme, voice
import assets.config as cf

from functools import partial
import aiohttp
import asyncio

import googletrans
#import gtts
import re

import random
import json
import os

from datetime import datetime

chain = markov.Model(cf.path, threshold=cf.threshold)

class Chatter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ookam = False
        self.translator = googletrans.Translator()
        
        self.dump_model.start()
        
    @tasks.loop(seconds=10.0)
    async def dump_model(self):
        await chain.expand()
        await chain.save()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        context = await self.bot.get_context(message)
        if context.valid:
            if message.author.bot:
                await context.invoke()

            if not context.command.name in cf.commands_and_chat:
                return
            
        text = re.sub("<@(!?)([0-9]*)>", "", message.content)
        #author = message.author
        
        # react to a message when ping
        if self.bot.user in message.mentions:
            sentence = await chain.generate(text)
            
            if message.channel.id in (864916234725097502, 908126832535154698): #tower-of-babel
                async with message.channel.typing():
                    detected = self.translator.detect(text)
                    #print(text, " -> ", detected.lang)
                    sentence = self.translator.translate(sentence, dest=detected.lang).text

            if "voice" in text.lower(): # voice mode
                if message.author.voice:
                    tts_text = re.sub(cf.discord_regex, "", sentence)
                    await voice.tts(tts_text, message.author.voice.channel)
 
            await message.reply(sentence, mention_author=False)
            
        elif self.ookam or message.channel.id == 887351509539500042 and message.author.id == 868768802370879558: # ookambot
            sentence = await chain.generate(text)
            sentence = "<@868768802370879558> " + sentence

            await asyncio.sleep(random.randint(1, 10))
            await message.reply(sentence)
         
        # add message to memory
        if message.author.bot:
            return
        if message.channel.id in cf.blacklist:
            return
        
        if message.guild.id != 803282468798201927:
            return
        
        await chain.add(text)

    @commands.command()
    @commands.is_owner()
    async def pingookam(self, ctx, state=""):
        if state.lower() in ("on", "y"):
            self.ookam = True
        elif state.lower() in ("off", "n"):
            self.ookam = False
        else:
            await ctx.send("wrong state, please use either 'on' or 'off' for the command")
            return

        await ctx.send(f"saved pingookam state to '{state}'")

class Impersonation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhooks = None

        self.offender = None
        self.koronbot = None

        self.load_webhooks()
        self.save_webhooks.start()

    def load_webhooks(self):
        with open(cf.webhook_path, "r") as f:
            self.webhooks = json.load(f)

    @tasks.loop(seconds=10.0)
    async def save_webhooks(self):
        with open(cf.webhook_path, "w") as f:
            json.dump(self.webhooks, f)

    @commands.command()
    async def impersonate(self, ctx, member: User = None, *, message = None):
        if ctx.guild.id == 803282468798201927:
            if not self.offender:
                self.offender = utils.get(ctx.guild.roles, id=1086894336437919835)
            
            if self.offender in ctx.author.roles:
                if message:
                    return await ctx.send(f"no embed perms exploit for you {ctx.author.name}!")

        auth = self.webhooks.get(str(ctx.channel.id)) # webhook authencation stuff
        message = message or await chain.generate()
        member = member or ctx.author

        if "@everyone" in message:
            return await ctx.send(f"no. fuck you {ctx.author.name}.")
        
        if "@here" in message:
            return await ctx.send(f"no. fuck you {ctx.author.name}.")

        """
        if member.id == 438145693824057355 and ctx.author.id != 438145693824057355: # rapdogg_
            await ctx.send("Due to the request of the almighty emperor, I am not able to impersonate the lord. I sincerely apologize, and I hope that the request does not block the joy.")
            return
        """
        session = aiohttp.ClientSession()
    
        if not auth:
            webhook = await ctx.channel.create_webhook(name = f"#{ctx.channel.name} Impersonation Webhook")
            self.webhooks[str(ctx.channel.id)] = {"id": webhook.id, "token": webhook.token}
        else:
            webhook = Webhook.partial(
                id = auth.get("id"), 
                token = auth.get("token"), 
                adapter = AsyncWebhookAdapter(session)
            )
            
        """
        if ctx.guild.id == 874326124501532693: # okbuddybaka
            message = re.sub(cf.discord_regex, "", message)
        """
        
        await ctx.message.delete()
        await webhook.send(
            message, 
            avatar_url = member.avatar_url, 
            username = member.name,
            allowed_mentions = AllowedMentions.none()
        )
        await session.close()
    
    """
    @commands.command()
    async def delete(self, ctx):
        if ctx.message.reference:
            if ctx.message.reference.resolved:
                reply = ctx.message.reference.resolved

                webhook_id = reply.webhook_id if reply.webhook_id else 0
                webhook_ids = [webhook["id"] for webhook in self.webhooks.values()]
                
                if webhook_id in webhook_ids:
                    await reply.delete()
                    #await ctx.message.delete()
                    await ctx.message.add_reaction(cf.approb)
    
    @commands.command(aliases=["leave"])
    async def fakekick(self, ctx, victim: User = None):
        if ctx.guild.id != 803282468798201927:
            return await ctx.send("sorry, this command is for okbh peeps only! :( but you can try using `pd impersonate` with your bot that kicks people!")
        
        if not self.koronbot:
            self.koronbot = utils.get(ctx.guild.members, id=804301771438555156)
        
        person = victim or ctx.author      
        auth = self.webhooks.get("935543814335107152") # webhook for #general
        
        session = aiohttp.ClientSession()
        webhook = Webhook.partial(
            id = auth.get("id"), 
            token = auth.get("token"), 
            adapter = AsyncWebhookAdapter(session)
        )
        message = cf.kickmsg.format(str(person), str(person.id))

        await ctx.message.delete()
        await webhook.send(message, avatar_url=self.koronbot.avatar_url, username=self.koronbot.name)
        await session.close()
    
    @commands.command()
    async def gold(self, ctx, victim: User = None):
        person = victim or ctx.author
        auth = self.webhooks.get(str(ctx.channel.id)) # webhook authencation stuff
        
        session = aiohttp.ClientSession()
        
        if not auth:
            webhook = await ctx.channel.create_webhook(name = f"#{ctx.channel.name} Impersonation Webhook")
            self.webhooks[str(ctx.channel.id)] = {"id": webhook.id, "token": webhook.token}
        else:
            webhook = Webhook.partial(
                id = auth.get("id"), 
                token = auth.get("token"), 
                adapter = AsyncWebhookAdapter(session)
            )
        
        embed = Embed(
            description=cf.gold.format(ctx.guild.name, ctx.guild.name),
            colour=Colour.red()
        )
        await ctx.message.delete()
        await webhook.send(embed=embed, avatar_url=person.avatar_url, username=person.name)
        await session.close()

    @commands.Cog.listener("on_command_error")
    async def webhook_issues(self, ctx, err):
        pass
    """
    
class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.templates = os.listdir(cf.templates_path)
    
    @commands.command()
    async def meme(self, ctx):
        await ctx.send("Making a very funny meme, please wait...")
        async with ctx.typing():
            template = cf.templates_path + random.choice(self.templates)
            text = await chain.generate(length=200)
            up, down = text[:len(text) // 2], text[len(text) // 2:]

            fn = partial(meme.make_meme, up, down, template)
            frames = await self.bot.loop.run_in_executor(None, fn)

            file = await meme.convert_to_file(frames)
            await ctx.message.reply(file=file)

class Pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_for_time.start()

    @tasks.loop(seconds=1)
    async def check_for_time(self):
        now = datetime.now()
        if now.minute == 00 and now.second == 00:
            await self.ping_role()

    async def ping_role(self):
        channel = self.bot.get_channel(882196471175331870) #hell
        guild = self.bot.get_guild(803282468798201927) # okbuddyhololive
        role = utils.get(guild.roles, id=882195759322259466) # '@fuck you' role

        text = await chain.generate() 
        message = await channel.send(role.mention + " " + text)
        await message.delete()

def setup(bot):
    bot.add_cog(Chatter(bot))
    bot.add_cog(Impersonation(bot))
    #bot.add_cog(Meme(bot))
    bot.add_cog(Pinger(bot))
