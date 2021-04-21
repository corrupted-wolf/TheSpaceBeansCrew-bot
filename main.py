import discord
import json
from keep_alive import keep_alive
from discord.ext import commands, tasks
import random
import os
from itertools import cycle
import time
import asyncio
from discord.utils import get

status = cycle(['eating some red meat', 'drinking succulent fresh water', 'checking 3 servers', 'checking your messages'])

no_words = ["slut", "fag", "faggot", "fuck you", "Donald Trump", "hoe", "mother fucker", "bitch", "Bitch", "wolfs are bad", "wolves are bad"]

def get_prefix(client, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]






client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
  change_status.start()

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
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@clear.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the permission required to use this command.')

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, error):
 if isinstance(error, commands.CommandNotFound):
   await ctx.send('This command does not exist.')
   print("an unknown command has been typed")


def is_it_me(ctx):
  return ctx.author.id == 625564753187831808

@client.command()
async def I(ctx):
  await ctx.send(f"Hi you are {ctx.author.mention}!")
  

@_8ball.error
async def _8ball_error(ctx, error):
  await ctx.send('please imput a question in your command')


@client.command(aliasses=["who is your creator"])
async def who_is_your_creator(ctx):
  await ctx.send("My creator is <@!62556475318783180>")


@client.event
async def Missing_Permission_error(ctx, error):
  await ctx.print("a permission is missing to complete this command please check the description of this bot on top.gg ")


@client.event
async def on_message(message):
  
  id = client.get_guild(809852942815199242)
  if any(word in message.content for word in no_words):
        await message.delete()
        await message.channel.send("""That Word Is Not Allowed To Be Used! Continued Use Of Mentioned Word Would Lead To Punishment!                                                                                                                                                                    You are welcomed and encouraged to read the rules of this server in the channel <#810165908530135041> . <@&833840805407883284>""")
  else:
       await client.process_commands(message)




keep_alive()
client.run('ODMyODAyODA1MjgxNDU2MTQ4.YHpGDQ.DEIvWAbsWtUqTc2eGRK0Zk1LlZk')