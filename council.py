import os
import discord
from discord.ext import commands
import asyncio

description = '''The council will decide your fate.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.command()
async def council(ctx, member: discord.Member):
    """Calls upon the council to determine the target user's fate."""

    vote_message = await ctx.send('Cast your vote. Silence {0.name}?'.format(member))
    # add reactions for voting
    await vote_message.add_reaction('✅')
    await vote_message.add_reaction('❌')

    # get reactions
    await asyncio.sleep(60)
    cache_msg = discord.utils.get(bot.cached_messages, id=vote_message.id)
    reactions = cache_msg.reactions
    for reaction in reactions:
        if reaction.emoji == '✅':
            yesses = reaction.count
        elif reaction.emoji == '❌':
            nos = reaction.count
    if yesses > nos and yesses > 2:
        await member.edit(mute = True, reason = "The council has spoken.")
        await ctx.send('The council has spoken. {0.name} has been judged unworthy.'.format(member))
    elif yesses > nos and yesses == 2:
        await ctx.send('The council could not come to a consensus. {0.name} is spared.'.format(member))
    else:
        await ctx.send('The council has spoken. {0.name} is spared.'.format(member))
    await ctx.send('{0} for, {1} against.'.format(yesses, nos))

@bot.command()
async def spare(ctx, member: discord.Member):
    """Calls upon the council to spare the target user."""

    vote_message = await ctx.send('Cast your vote. Spare {0.name}?'.format(member))
    # add reactions for voting
    await vote_message.add_reaction('✅')
    await vote_message.add_reaction('❌')

    # get reactions
    await asyncio.sleep(60)
    cache_msg = discord.utils.get(bot.cached_messages, id=vote_message.id)
    reactions = cache_msg.reactions
    for reaction in reactions:
        if reaction.emoji == '✅':
            yesses = reaction.count
        elif reaction.emoji == '❌':
            nos = reaction.count
    if yesses > nos and yesses > 2:
        await member.edit(mute = False, reason = "The council has spoken.")
        await ctx.send('The council has spoken. {0.name} has been spared.'.format(member))
    elif yesses > nos and yesses == 2:
        await ctx.send('The council could not come to a consensus. {0.name} shall remain silenced.'.format(member))
    else:
        await ctx.send('The council has spoken. {0.name} shall remain silenced.'.format(member))
    await ctx.send('{0} for, {1} against.'.format(yesses, nos))

bot.run(os.environ['BOT_KEY'])
