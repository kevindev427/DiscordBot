import logging
from logging.handlers import RotatingFileHandler
import random
import time
import datetime
import sys
import asyncio
from collections import Counter
from pytz import timezone
import discord
from discord.ext import commands
import loadconfig

__version__ = '0.11.2'

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(filename='discordbot.log', maxBytes=1024*5, backupCount=2, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''Der-Eddys deutscher Discord Bot, programmiert mit Discord.py'''
bot = commands.Bot(command_prefix=loadconfig.__prefix__, description=description)

def _currenttime():
    return datetime.datetime.now(timezone('Europe/Berlin')).strftime('%H:%M:%S')

async def _randomGame():
    #Check games.py to change the list of "games" to be played
    while True:
        randomGame = random.choice(loadconfig.__games__)
        logging.info(f'Changing name to {randomGame}')
        await bot.change_presence(game=discord.Game(name=randomGame))
        await asyncio.sleep(loadconfig.__gamesTimer__)

@bot.event
async def on_ready():
    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    print('------')
    for cog in loadconfig.__cogs__:
        try:
            bot.load_extension(cog)
        except Exception:
            print(f'Couldn\'t load cog {cog}')
    bot.commands_used = Counter()
    bot.startTime = time.time()
    bot.botVersion = __version__
    bot.owner = discord.utils.find(lambda u: u.id == loadconfig.__adminid__, bot.get_all_members())
    bot.gamesLoop = asyncio.ensure_future(_randomGame())

@bot.event
async def on_command(command, ctx):
    bot.commands_used[command.name] += 1
    msg = ctx.message
    if msg.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(msg)
    logging.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(msg, destination))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        await bot.add_reaction(message, '👀') # :eyes:
    if 'loli' in message.clean_content.lower():
        await bot.add_reaction(message, '🍭') # :lollipop:
    if 'league of legends' in message.clean_content.lower():
        await bot.add_reaction(message, '💩') # :poop:
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ == 'True':
            emojis = [':wave:', ':congratulations:', ':wink:', ':new:', ':cool:', ':white_check_mark:', ':tada:']
            await bot.send_message(member.server.default_channel, '{0} Willkommen {1} auf Der-Eddys Discord Server! Für weitere Informationen, wie unsere nsfw Channel :underage: , besuche unseren <#165973433086115840> Channel.'.format(random.choice(emojis), member.mention))

@bot.event
async def on_member_remove(member):
    if member.server.id == loadconfig.__botserverid__:
        memberExtra = '{0} - *{1} ({2})*'.format(member.mention, member, member.id)
        if loadconfig.__greetmsg__ == 'True':
            await bot.send_message(member.server.default_channel, f'<:faeSad:298772756127023104> {member.mention} verließ unseren Server')

@bot.event
async def on_server_join(server):
    embed = discord.Embed(title=':white_check_mark: Server hinzugefügt', type='rich', color=0x2ecc71)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='Name', value=server.name, inline=True)
    embed.add_field(name='ID', value=server.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{server.owner} ({server.owner.id})', inline=True)
    embed.add_field(name='Region', value=server.region, inline=True)
    embed.add_field(name='Mitglieder', value=server.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=server.created_at, inline=True)
    await bot.send_message(bot.owner, embed=embed)

@bot.event
async def on_server_remove(server):
    embed = discord.Embed(title=':x: Server entfernt', type='rich', color=0xe74c3c)
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='Name', value=server.name, inline=True)
    embed.add_field(name='ID', value=server.id, inline=True)
    embed.add_field(name='Besitzer', value=f'{server.owner} ({server.owner.id})', inline=True)
    embed.add_field(name='Region', value=server.region, inline=True)
    embed.add_field(name='Mitglieder', value=server.member_count, inline=True)
    embed.add_field(name='Erstellt am', value=server.created_at, inline=True)
    await bot.send_message(bot.owner, embed=embed)

@bot.command(pass_context=True, hidden=True, aliases=['quit_backup'])
async def shutdown_backup(ctx):
    '''Fallback if mod cog couldn't load'''
    if ctx.message.author.id == loadconfig.__adminid__:
        await bot.say('**:ok:** Bye!')
        bot.logout()
        sys.exit(0)
    else:
        await bot.say('**:no_entry:** Du bist nicht mein Bot Besitzer!')

if __name__ == '__main__':
    bot.run(loadconfig.__token__)
