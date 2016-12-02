import random
import urllib.parse
import asyncio
import aiohttp
import discord
from discord.ext import commands

class fun():
    def __init__(self, bot):
        self.bot = bot

    def userOnline(self, memberList):
        online = []
        for i in memberList:
            if i.status == discord.Status.online and i.bot == False:
                online.append(i)
        return online

    @commands.command(aliases=['javascript', 'nodejs', 'js'])
    async def java(self):
        '''Weil Java != Javscript'''
        await self.bot.say(':interrobang: Meintest du jQuery, Javascript oder Node.js? https://abload.de/img/2016-05-102130191kzpu.png')

    @commands.command(aliases=['c++', 'c', 'c#', 'objective-c'])
    async def csharp(self):
        '''Wie soll man da überhaupt durchblicken???'''
        await self.bot.say(':interrobang: Meintest du C, C++, C# oder Objective-C? https://i.imgur.com/Nd4aAXO.png')

    @commands.command()
    async def praise(self):
        '''Praise the Sun'''
        await self.bot.say('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self):
        '''Counter Strike: Source'''
        await self.bot.say('http://i.imgur.com/TgPKFTz.gif')

    @commands.command()
    async def countdown(self):
        '''It's the final countdown'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await self.bot.say('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await self.bot.say('**:ok:** DING DING DING')

    @commands.command(aliases=['cat', 'randomcat'])
    async def neko(self):
        '''Zufällige Katzen Bilder nyan~'''
        #http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
        async with aiohttp.get('http://random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                msg = random.choice(emojis) + js['file']
                await self.bot.say(msg)


    @commands.command(pass_context=True, aliases=['rand'])
    async def random(self, ctx, *arg):
        '''Gibt eine zufällige Zahl oder Member aus

        Benutzung:
        -----------

        :random
            Gibt eine zufällige Zahl zwischen 1 und 100 aus

        :random coin
            Wirft eine Münze (Kopf oder Zahl)

        :random 6
            Gibt eine zufällige Zahl zwischen 1 und 6 aus

        :random 10 20
            Gibt eine zufällige Zahl zwischen 10 und 20 aus

        :random user
            Gibt einen zufällige Benutzer der gerade online ist aus
        '''
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Kopf', 'Zahl']
                await self.bot.say(':arrows_counterclockwise: {0}'.format(random.choice(coin)))
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.message.channel.server.members)
                randomuser = random.choice(online)
                if ctx.message.channel.permissions_for(ctx.message.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await self.bot.say(':congratulations: {0}'.format(user))
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) > 1:
                start = int(arg[0])
                end = int(arg[1])
            await self.bot.say('**:arrows_counterclockwise:** Zufällige Zahl ({0} - {1}): {2}'.format(start, end, random.randint(start, end)))

    @commands.command(pass_context=True)
    async def steinigt(self, ctx, *member:str):
        '''Monty Python'''
        await self.bot.say(member + '\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

    @commands.command(pass_context=True)
    async def giphy(self, ctx, *searchterm: str):
        '''Listet reaction Bilder von giphy.com
        Erlaubt r-rating Bilder in Channel die 'nsfw' beinhalten

        Beispiel:
        -----------

        :giphy ghibli
        '''
        searchstring = urllib.parse.quote_plus(' '.join(searchterm))
        apikey = 'dc6zaTOxFJmzC'
        limit = 4
        if 'nsfw' in ctx.message.channel.name:
            rating = 'r'
        else:
            rating = 'pg-13'
        async with aiohttp.get('https://api.giphy.com/v1/gifs/search?q={}&api_key={}&limit={}&rating={}'.format(searchstring, apikey, limit, rating)) as r:
            if r.status == 200:
                js = await r.json()
                randomint = random.randint(0, js['pagination']['count'] - 1)
                #doesn't work well with random reactions :|
                #emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
                msg = js['data'][randomint]['url']
                await self.bot.say(msg)

    @commands.command(aliases=['hypu', 'train'])
    async def hype(self):
        '''HYPE TRAIN CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = ':train2: CHOO CHOO {}'.format(random.choice(hypu))
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def xkcd(self, ctx,  *searchterm: str):
        '''Zeigt den letzten oder zufääligen XKCD Comic

        Beispiel:
        -----------

        :xkcd

        :xkcd random
        '''
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.get(apiUrl.format('/')) as r:
            if r.status == 200:
                js = await r.json()
                if ''.join(searchterm) == 'random':
                    randomComic = random.randint(0, js['num'])
                    async with aiohttp.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await self.bot.say(msg)

    @commands.command(pass_context=True, alias=['r', 'addreaction'])
    async def reaction(self, ctx, emojiname: str, *messageid : str):
        '''Fügt der letzten Nachricht ein Emoji als Reaction hinzu oder einer bestimmten Nachricht

        Beispiel:
        -----------
        :reaction ok_hand

        :addreaction sunglasses 247386709505867776
        '''
        emojifind = discord.utils.find(lambda e: e.name.lower() == emojiname.lower(), self.bot.get_all_emojis())
        if emojifind:
            emoji = emojifind
        else:
            emoji = emojiname
        if not messageid:
            async for msg in self.bot.logs_from(ctx.message.channel, limit=1, before=ctx.message):
                message = msg
        else:
            message = await self.bot.get_message(ctx.message.channel, messageid[0])
        if message:
            await self.bot.add_reaction(message, emoji)
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say('**:x:** Konnte keine Nachricht mit dieser ID finden!')

def setup(bot):
    bot.add_cog(fun(bot))
