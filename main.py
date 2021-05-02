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
from datetime import datetime



def get_prefix(client, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix)
client.remove_command("help")
@client.event
async def on_ready():
  change_status.start()


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
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)
  
  prefixes[str(ctx.guild.id)] = prefix


  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)
 
  await ctx.send(f'prefix changed to: {prefix}')

status = cycle(['eating some red meat', 'drinking succulent fresh water', 'checking 4 servers', 'checking your messages', f"s!help"])



@client.command()
async def help(ctx):
  th = discord.Embed(
    title = f"Commands",
    description = f"The current prefix set is `{ctx.prefix}` if you want more info on a command type `help_command`.",
    colour = discord.Colour.teal())

  th.set_footer(text="Thank you for using this bot!")
  th.set_thumbnail(url="https://imgur.com/zYvNqYX.png")
  th.set_author(name="Creator: Corrupted wolf/×", icon_url="https://imgur.com/Ov7gmm7.png")

  th.add_field(name="‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎Moderator commands", value="commands for people with certain permissions (the bot is required to have these permissions as well to make these commands work.)", inline=False)
  th.add_field(name="clear", value=f"`{ctx.prefix}clear` ( manage message permission is required to use this command)", inline=False)
  th.add_field(name="changeprefix", value=f"`{ctx.prefix}changeprefix <your new prefix> `(the administrator permissions is required for this command, the bot does not need it)", inline=False)
  th.add_field(name=" ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎General commands", value=("commands for everyone to use!"), inline=False)
  th.add_field(name="ping", value=f"`{ctx.prefix}ping`", inline=False)
  th.add_field(name="8ball", value=f"`{ctx.prefix}8ball <your question>`", inline=False)
  th.add_field(name="I", value=f"`{ctx.prefix}I`", inline=False)
  th.add_field(name="who_is_your_creator", value=f"`{ctx.prefix}who_is_your_creator`", inline=False)
  th.add_field(name="random fact", value="`random_fact`", inline=False)
  th.add_field(name="whois", value=f"`{ctx.prefix}whois <person>`", inline = True)
  await ctx.send(embed = th)

@client.command()
async def help_clear(ctx):
  thc = discord.Embed(title = "clear", description = f"Erase the number of messages desired.(The permission manage messages is needed by the bot and the user of the command.)", colour = discord.Color.blue())

  thc.add_field(name="Syntax", value=f"`clear <amount of messages to delete>`", inline=False)

  await ctx.send(embed = thc)

@client.command()
async def help_changeprefix(ctx):
  thc = discord.Embed(title = "changeprefix", description = f"Changes the prefix set for this server.", colour = discord.Color.blue())

  thc.add_field(name="Syntax", value=f"`changeprefix <the new prefix>`", inline=False)

  await ctx.send(embed = thc)

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = ['It is certain.', 'Yes - definitely.', 'You may rely on it.', 'Yes.', 'Most likely.', 'My reply is no.', 'Cannot predict now.', 'My sources say no.', 'Ask again later.', 'As I see it yes.', 'Nah.', 'Yas.', 'Nevaaaa!', 'Duh.', 'You do not deserve an answer.']
  await ctx.send(f'Question:{question}\nAnswer: {random.choice(responses)}')

@client.command(aliases=["random fact"])
async def random_fact(ctx):
  responses = ["The speed of light is generally rounded down to 186,000 miles per second. In exact terms it is 299,792,458 m/s.", "It takes 8 minutes 17 seconds for light to travel from the Sun’s surface to the Earth.", "October 12th, 1999 was declared “The Day of Six Billion” based on United Nations projections.", "10 percent of all human beings ever born are alive at this very moment.", "The Earth spins at 1,000 mph but it travels through space at an incredible 67,000 mph.", "Every year over one million earthquakes shake the Earth.", "When Krakatoa erupted in 1883, its force was so great it could be heard 4,800 kilometres away in Australia.", "The largest ever hailstone weighed over 1kg and fell in Bangladesh in 1986.", "Every second around 100 lightning bolts strike the Earth., Every year lightning kills 1000 people.", "In October 1999 an Iceberg the size of London broke free from the Antarctic ice shelf .", "If you could drive your car straight up you would arrive in space in just over an hour.", "Human tapeworms can grow up to 22.9m.", "The Earth is 4.56 billion years old...the same age as the Moon and the Sun.", "The dinosaurs became extinct before the Rockies or the Alps were formed.", "Female black widow spiders eat their males after mating.", "When a flea jumps, the rate of acceleration is 20 times that of the space shuttle during launch.", "If our Sun were just inch in diameter, the nearest star would be 445 miles away.", "The Australian billygoat plum contains 100 times more vitamin C than an orange.", "Astronauts cannot belch – there is no gravity to separate liquid from gas in their stomachs.", "The air at the summit of Mount Everest, 29,029 feet is only a third as thick as the air at sea level.", "One million, million, million, million, millionth of a second after the Big Bang the Universe was the size of a ...pea.", "DNA was first discovered in 1869 by Swiss Friedrich Mieschler.", "The molecular structure of DNA was first determined by Watson and Crick in 1953.", "The first synthetic human chromosome was constructed by US scientists in 1997.", "The thermometer was invented in 1607 by Galileo.", "Englishman Roger Bacon invented the magnifying glass in 1250.", "Alfred Nobel invented dynamite in 1866.", "Wilhelm Rontgen won the first Nobel Prize for physics for discovering X-rays in 1895.", "The tallest tree ever was an Australian eucalyptus – In 1872 it was measured at 435 feet tall.", "Christian Barnard performed the first heart transplant in 1967 – the patient lived for 18 days.", "The wingspan of a Boeing 747 is longer than the Wright brother’s first flight.", "An electric eel can produce a shock of up to 650 volts.", "‘Wireless’ communications took a giant leap forward in 1962 with the launch of Telstar, the first satellite capable of relaying telephone and satellite TV signals.", "The earliest wine makers lived in Egypt around 2300 BC.", "The Ebola virus kills 4 out of every 5 humans it infects.", "In 5 billion years the Sun will run out of fuel and turn into a Red Giant.", "Giraffes often sleep for only 20 minutes in any 24 hours. They may sleep up to 2 hours (in spurts – not all at once), but this is rare. They never lie down.", "A pig’s orgasm lasts for 30 minutes.", "Without its lining of mucus your stomach would digest itself.", "Humans have 46 chromosomes, peas have 14 and crayfish have 200.", "There are 60,000 miles of blood vessels in the human body.", "An individual blood cell takes about 60 seconds to make a complete circuit of the body.", "Utopia ia a large, smooth lying area of Mars.", "On the day that Alexander Graham Bell was buried the entire US telephone system was shut down for 1 minute in tribute.", "The low frequency call of the humpback whale is the loudest noise made by a living creature.", "The call of the humpback whale is louder than Concorde and can be heard from 500 miles away.", "A quarter of the world’s plants are threatened with extinction by the year 2010.", "Each person sheds 40lbs of skin in his or her lifetime.", "At 15 inches the eyes of giant squids are the largest on the planet."]
  await ctx.send(f" Fact: {random.choice(responses)}")
 

@client.command()
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

@clear.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the permission required to use this command. You need the manage messages permission to use this command.')

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@tasks.loop(seconds=15)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, error):
 if isinstance(error, commands.CommandNotFound):
   await ctx.send('This command does not exist.')
   print("an unknown command has been typed")

@clear.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.BotMissingPermissions):
    await ctx.send('This command requires a permission this bot was not granted please check the description of this bot in top.gg')


def is_it_me(ctx):
  return ctx.author.id == 625564753187831808

@client.command(aliases=["user", "info"])
async def whois(ctx, member : discord.Member):
 whoemb = discord.Embed(title = member.name, description = member.mention, colour = discord.Colour.dark_gold())
 whoemb.add_field(name = "ID", value = member.id, inline = True)

 await ctx.send(embed=whoemb)
  
@client.command()
async def I(ctx):
  Iemb = discord.Embed(title =f"{ctx.author.name}", description =f"{ctx.author.mention}", colour = discord.Colour.gold())
  Iemb.add_field(name = "ID", value =f"{ctx.author.id}", inline = True )
  await ctx.send(embed = Iemb)

@_8ball.error
async def _8ball_error(ctx, error):
  await ctx.send('please imput a question in your command')


@client.command(aliasses=["who is your creator"])
async def who_is_your_creator(ctx):
  await ctx.send("My creator is <@625564753187831808>")


my_secret = os.environ['Token']


keep_alive()
client.run((my_secret))