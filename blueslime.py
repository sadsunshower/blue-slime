#!/usr/bin/env python3

import config, profile

import discord.ext.commands

import sys

bot = discord.ext.commands.Bot(command_prefix='?')

@bot.command()
async def run(ctx, key: str) -> None:
    if ctx.channel.id not in config.get_channels():
        await ctx.channel.send('Not authorised to run in this channel!')
        return

    profile = config.get_profile(key)

    if profile is None:
        await ctx.channel.send(f'Unknown profile `{key}`')
        return

    profile.run()
    await ctx.channel.send(f'Running profile `{key}`')

@bot.command()
async def console(ctx, key: str, *args) -> None:
    if ctx.channel.id not in config.get_channels():
        await ctx.channel.send('Not authorised to run in this channel!')
        return

    profile = config.get_profile(key)

    if profile is None:
        await ctx.channel.send(f'Unknown profile `{key}`')
        return

    if not profile.running():
        await ctx.channel.send(f'Profile `{key}` is not running, start it with `?run`')
        return

    if not profile.console_allowed():
        await ctx.channel.send(f'Profile `{key}` does not allow console access')
        return

    profile.console(' '.join(args))
    await ctx.channel.send('Sent console input!')

@bot.command()
async def check(ctx, key: str) -> None:
    if ctx.channel.id not in config.get_channels():
        await ctx.channel.send('Not authorised to run in this channel!')
        return

    profile = config.get_profile(key)

    if profile is None:
        await ctx.channel.send(f'Unknown profile `{key}`')
        return

    if profile.running():
        await ctx.channel.send(f'`{key}` is running')
    else:
        await ctx.channel.send(f'`{key}` has stopped')

@bot.command()
async def kill(ctx, key: str) -> None:
    if ctx.channel.id not in config.get_channels():
        await ctx.channel.send('Not authorised to run in this channel!')
        return

    profile = config.get_profile(key)

    if profile is None:
        await ctx.channel.send(f'Unknown profile `{key}`')
        return

    if not profile.running():
        await ctx.channel.send(f'Profile `{key}` is already not running')
        return

    profile.kill()
    await ctx.channel.send(f'Killed `{key}`!')

if not config.load_config():
    print('No config file found! New one created @ config.json. Please fill it out and run me again!')
    sys.exit(1)

bot.run(config.get_token())