from aiofile import async_open
import markovify
import msgpack
import random
import nltk

class Model:
    def __init__(self, path, threshold=200):
        self.path = path
        self.threshold = threshold
        self.mem_len = 20000
        
        self.memory = []
        self.chain = None

        self.load()
    
    def load(self):
        with open(self.path, "rb") as f:
            self.memory = msgpack.load(f)
        
        length = len(self.memory)
        slice = length - self.mem_len
        
        if length > self.mem_len:
            self.memory = self.memory[slice:]
        
    async def save(self):
        async with async_open(self.path, "wb") as f:
            await f.write(msgpack.dumps(self.memory))
    
    async def expand(self):
        self.chain = markovify.NewlineText(self.memory, well_formed=False)
    
    async def add(self, text):
        self.memory.append(text)
        
        if len(self.memory) > self.mem_len:
            self.memory = self.memory[1:]
    
    async def keyword(self, text):
        wordlist = nltk.pos_tag(text.split())
        keyword = ""

        nouns = [word[0] for word in wordlist if word[1] == "NN"]
        wordlist = dict(wordlist)

        if nouns:
            keyword = random.choice(nouns)
        else:
            keyword = random.choice(list(wordlist.keys()))

        return keyword + " "
    
    async def generate(self, text="", length=2000):
        if not len(text):
            chain = self.chain
        else:
            keyword = await self.keyword(text)
            temp_mem = [x for x in self.memory if keyword in x]
            
            if len(temp_mem) < self.threshold:
                chain = self.chain
            else:
                chain = markovify.NewlineText(temp_mem, well_formed=False)
                
        return chain.make_short_sentence(length)