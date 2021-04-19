import discord
from discord.ext import commands




class Mods(commands.cog):


  def __init__(self, client):
    self.client = client
#Events
  @commands.Cog.listener()
  async def on_ready(self):
    print('bot is online')
#Commands
  @commands.command()
  async def ping(self, ctx):
   await ctx.send('pong!')



def setup(client):
  client.add_cog(Mods(client))