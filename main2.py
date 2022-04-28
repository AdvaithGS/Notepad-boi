import disnake as discord 
from disnake.ext import commands

bot = commands.Bot("!", sync_commands_debug=True)


@bot.event
async def on_ready():
  print("The bot is ready!")


@bot.event
async def on_message(message):
  ctx = message.channel
  mes = message.content[23:]
  if mes.startswith('hi'):
    await ctx.send('hello there')


guild_ids = [808201667543433238]
channels = [808201667543433241]


async def check():
  for channel in channels:
    await bot.get_channel(channel).send(content = 'Is this working?')

@bot.slash_command(guild_ids = guild_ids)
async def this(
  ctx,
  place : str ,
  number : int):
  '''
    Returns that.

    Parameters
    ----------
    place: class `str` 
      The location whose thing you want to see
    amount: class `int` 
      Your favourite number
  '''
  embed = discord.Embed(title = place,description = number, colour = discord.Color.orange())
  await ctx.response.send_message(embed = embed)
  await check()

bot.run(os.environ[''])