import discord
import json
from keep_alive import keep_alive
from discord.ext import commands, tasks
import random
import os
from itertools import cycle
from discord.ext import has_permission

status = cycle(['Status 1', 'Status 2', 'Status 3'])


def get_prefix(client, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]
  
client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('eating meat'))
  print('we have logged in as {0.user}'.format(client))
  
@client.event
async def on_guild_join(guild):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)
  
  prefixes[str(guild.id)] = 's!'


  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)
  
  prefixes.pop(str(guild.id))

  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)
  
  prefixes[str(ctx.guild.id)] = prefix


  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)
 
  await ctx.send(f'prefix changed to: {prefix}')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = ['It is certain.', 'Yes - defenitely.', 'You may rely on it.', 'Yes.', 'Most likely.', 'My reply is no.', 'Cannot predict now.', 'My sources say no.', 'Ask again later.', 'As I see it yes.', 'Nah.', 'Yas.', 'Nevaaaa!', 'Duh.', 'You do not deserve an answer.']
  await ctx.send(f'Question:{question}\nAnswer: {random.choice(responses)}')



@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


keep_alive()
client.run('ODMyODAyODA1MjgxNDU2MTQ4.YHpGDQ.WYuT_y3pDODpk_wcZPs3DTdkNY0')