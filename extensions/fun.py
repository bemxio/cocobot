# pylint: disable=import-error
# pylint: disable=no-member

from discord.ext import commands, tasks
from discord import utils, User

from assets.modules import voice
import assets.config as cf

import random
import json

def random_chance(percent, max=100):
    return random.randint(0, max) <= percent

def make_ip_num(c: str) -> str:
    random.seed(ord(c))
    return str(random.randint(0, 255))

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        with open("assets/gifs/huggies.json", "r") as f:
            self.hugs = json.load(f)
        
        with open("assets/gifs/kisses.json", "r") as f:
            self.kisses = json.load(f)
        
        with open("assets/gifs/pats.json", "r") as f:
            self.pats = json.load(f)

        with open("assets/gifs/slaps.json", "r") as f:
            self.slaps = json.load(f)

    @commands.command()
    async def hug(self, ctx, member: User = None):
        if ctx.channel.id in cf.erp_channels:
            return await ctx.send(cf.reaction_command_fail)
        
        hugger = ctx.author
        member = member or hugger

        hug = random.choice(self.hugs)
        if hugger.id == cf.crimid and member.id == cf.crimid:
            await ctx.message.reply(cf.crimhug + hug, mention_author=False)
        elif member.id == self.bot.user.id:
            await ctx.message.reply(cf.cocobothug + hug, mention_author=False)
        elif member == hugger:
            await ctx.message.reply(cf.selfhug + hug, mention_author=False)
        else:
            await ctx.message.reply(cf.hug.format(member.mention, hugger.name) + hug, mention_author=False)
    
    @commands.command()
    async def kiss(self, ctx, member: User = None):
        if ctx.channel.id in cf.erp_channels:
            return await ctx.send(cf.reaction_command_fail)
        
        kisser = ctx.author
        member = member or kisser

        kiss = random.choice(self.kisses)
        if kisser.id == cf.crimid and member.id == cf.crimid:
            await ctx.message.reply(cf.crimkiss + kiss, mention_author=False)
        elif member.id == self.bot.user.id:
            await ctx.message.reply(cf.cocobotkiss + kiss, mention_author=False)
        elif member == kisser:
            await ctx.message.reply(cf.selfkiss + kiss, mention_author=False)
        else:
            await ctx.message.reply(cf.kiss.format(member.mention, kisser.name) + kiss, mention_author=False)

    @commands.command()
    async def slap(self, ctx, member: User = None):
        slapper = ctx.author
        member = member or slapper

        slap = random.choice(self.slaps)
        if member.id == self.bot.user.id:
            await ctx.message.reply(cf.cocobotslap + slap, mention_author=False)
        elif member == slapper:
            await ctx.message.reply(cf.selfslap + slap, mention_author=False)
        else:
            await ctx.message.reply(cf.slap.format(member.mention, slapper.name) + slap, mention_author=False)
    
    @commands.command()
    async def pat(self, ctx, member: User = None):
        patter = ctx.author
        member = member or patter

        pat = random.choice(self.pats)
        if patter.id == cf.crimid and member.id == cf.crimid:
            await ctx.message.reply(cf.crimpat + pat, mention_author=False)
        elif member.id == self.bot.user.id:
            await ctx.message.reply(cf.cocobotpat + pat, mention_author=False)
        elif member == patter:
            await ctx.message.reply(cf.selfpat + pat, mention_author=False)
        else:
            await ctx.message.reply(cf.pat.format(member.mention, patter.name) + pat, mention_author=False)

class Clips(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clips = self.load_clips()
        
    def load_clips(self, path="assets/clips.txt"):
        with open(path, "r") as file:
            clips = file.readlines()
            
        clips = [clip for clip in clips if not clip.startswith("#")] # filter out comments
        return clips

    @commands.command()
    async def clip(self, ctx):
        clip = random.choice(self.clips)
        quote = random.choice(cf.graduation)
        
        await ctx.send(clip + " " + quote)

class OtherFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.insults = self.load_insults()
        self.compliments = self.load_compliments()

        self.ratios = self.load_ratio()
        self.reactions = ["🔥", "<:0hesright:826211392335904809>", "<:WataTrue:899474236123525180>", "<:_RedditUpvote:817785593152405506>", "💯", "🥶", "📠", "🗣️"]
    
    def load_insults(self):
        with open("assets/insults.txt", "r") as f:
            insults = f.read()

        insults = [insult for insult in insults.split("\n") if not insult.startswith("#")]
        return insults

    def load_compliments(self):
        with open("assets/compliments.txt", "r") as f:
            compliments = f.read()

        compliments = [compliment for compliment in compliments.split("\n") if not compliment.startswith("#")]
        return compliments
    
    def load_ratio(self):
        with open("assets/ratio.txt", "r") as f:
            ratio = f.read()

        ratio = [ratio for ratio in ratio.split("\n") if not ratio.startswith("#")]
        return ratio

    @commands.Cog.listener()
    async def on_message(self, message):
        if cf.someone in message.content:
            members = message.guild.members

            random_member = random.choice(members)
            while random_member.bot:
                random_member = random.choice(members)
        
            await message.channel.send(random_member.mention)
        
        if message.author.bot:
            return
        
        if "!gm" in message.content: # good morning motherf*ckers
            if random_chance(25):
                if message.author.voice:
                    with open("assets/gm_mfs.mp3", "rb") as f:
                        await voice.play(f, message.author.voice.channel)
                else:
                    await message.channel.send("https://cdn.discordapp.com/attachments/816054459679113249/853313601577812037/gm_mfs.mp4")
        
        if "faggot" in message.content or "gay" in message.content: # coco says gay slur
            if random_chance(25):
                if message.author.voice:
                    with open("assets/faggot.mp3", "rb") as f:
                        await voice.play(f, message.author.voice.channel)

    @commands.command()
    async def saytts(self, ctx, *, message):
        if ctx.author.voice: # if user isn't in a voice channel
            await voice.tts(message, ctx.author.voice.channel)
        else:
            await ctx.message.reply("Join a voice channel to use this command!", mention_author=False)

    @commands.command()
    async def impregnate(self, ctx):
        if random_chance(1) or ctx.author.id == 425316155863990272:
            await ctx.author.send(cf.impregnate)
    
    @commands.command()
    async def sex(self, ctx, member: User = None):
        if member:
            return await ctx.send(cf.grooming.format(ctx.author.name.lower(), member.name.lower()))
            
        await ctx.send(cf.sex.format(ctx.author.name.lower()))
    
    @commands.command()
    async def doxx(self, ctx, member: User = None):
        victim = member or ctx.author
        name = victim.display_name
        
        if victim == self.bot.user:
            return await ctx.send(cf.cocodoxx.format(ctx.author))
        
        # getting every nth character
        if len(name) < 4: # less than enough needed
            while len(name) < 4:
                name += name[-1] # add last character to variable until len is more than 4      
            
        chars = list(map(make_ip_num, name))
        while len(chars) > 4:
            chars.pop()
        
        ip = ".".join(chars)
        
        if victim == ctx.author:
            await ctx.send(cf.doxx.format(
                "Your",
                ip,
                victim.mention
            ))
        else:
            await ctx.send(cf.doxx.format(
                victim.name,
                ip,
                victim.mention
            ))

    @commands.command()
    async def rape(self, ctx):
        await ctx.send(cf.rape)
    
    @commands.command()
    async def insult(self, ctx, person: User = None):
        """
        if ctx.guild.id == 803282468798201927:
            return await ctx.message.reply("Due to the recent server strike, I can't insult holotards here <:0Gilgamesh:867480201826140182>")
        """
        person = person or ctx.author
        insult = random.choice(self.insults)
        
        if random_chance(25):
            insult += " 💀"
            
        await ctx.send(person.mention + " " + insult)
     
    @commands.command()
    async def ratio(self, ctx):
        ratio = random.choice(self.ratios)
        
        message = await ctx.send(ratio)
        for reaction in random.sample(self.reactions, len(self.reactions)):
            await message.add_reaction(reaction)
    
    @commands.command()
    async def compliment(self, ctx, person: User = None):
        person = person or ctx.author
        compliment = random.choice(self.compliments)
            
        if random_chance(25):
            compliment += " <3"
        
        await ctx.send(person.mention + " " + compliment)

def setup(bot):
    bot.add_cog(Reactions(bot))
    bot.add_cog(Clips(bot))
    bot.add_cog(OtherFun(bot))
