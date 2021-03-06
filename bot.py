import discord
from discord.ext import commands
import pickle
import random
import io
import os
import sys
import traceback
import datetime
import pynite
import textwrap
from contextlib import redirect_stdout
from ext.utility import developer
import asyncio
import json

bot = commands.Bot(command_prefix="$", description="A simple bot created in discord.py library by Nyan Pikachu#4148 for moderation and misc commands!", owner_id=279974491071709194)

bot.load_extension("cogs.info")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.fortnite")
bot.load_extension("cogs.pokedex")
bot.load_extension("cogs.cr")

#eval!!!
def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

#developer check
def developer():
    def wrapper(ctx):
        with open('data/devlist.json') as f:
            devs = json.load(f)
        if ctx.author.id in devs:
            return True
        raise commands.MissingPermissions('Sorry, this command is only available for developers.')
    return commands.check(wrapper)
    

devs = [
    279974491071709194,
    199436790581559296
]

@bot.command()
@developer()
async def eval(ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }
        
        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')            
                
@bot.event
async def on_ready():
    print("Bot is online!")
    x = bot.get_channel(424677910314745856)
    now = datetime.datetime.utcnow()
    await x.send('Bot is online :thumbsup: at ' + now.strftime("%A, %d. %B %Y %I:%M%p") )

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    def check(reaction, user):
        return user != reaction.message.author and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        em = discord.Embed(color=discord.Color.gold())
        head = f'{reaction.emoji}  {reaction.count} {reaction.message.channel} ID: {reaction.message.id}'
        em.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)
        em.description = reaction.message.content
        await channel.send(head, embed=em)
        reaction, user = await bot.wait_for('reaction_remove', timeout=60.0, check=check)
        await message.edit(embed=em)
        reaction, user = await bot.wait_for('reaction_clear', timeout=60.0, check=check)
        await message.delete(embed=em)
    except asyncio.TimeoutError:
        pass
    else:
        await ctx.send("i tried :shrug:")

@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
    await ctx.send(embed=em)

@bot.command(name='presence')
@developer()
async def _presence(ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.streaming))
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.playing))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.listening))
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await bot.change_presence(activity=discord.Activity(name=None))
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 

bot.run(os.environ.get("TOKEN"))