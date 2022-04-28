import disnake as discord
import os
client = discord.Client()
from keep_alive import keep_alive
from sqlitedict import SqliteDict
db = SqliteDict('./db.sqlite')
keys = db.keys()
values = db.values()
from bs4 import BeautifulSoup
import requests
@client.event
async def on_guild_join(guild):
  channel = await guild.create_text_channel('Tha-NotePad-Boi')
  await channel.send('Welcome to the notepad bot, you have been registered and this server can use the common notepad. Use `$help` to see all available commands.')
  db[guild.id] = ''

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message): 
  ctx = message.channel  
  author = message.author.discriminator

  if message.content.startswith("$signup"):
    content = message.content
    password = content.strip('$signup')
    if (author in keys) == True:
      await message.channel.send('You already have an account! Log in using `$login (password)`')
    if (author in keys) == False:
      if password == '' or password ==' ':
        await message.channel.send('You have to write a password following $signup, like `$signup (password)`')
      db[author] = password
      await message.channel.send('Signed up.')
    return

  elif message.content.startswith('$login'):
    content = message.content
    password = content.strip('$login')
    if (author in keys) == True:
      actual = db[author]
      if actual == password:
        await message.channel.send('Logged in')
        db[author] = password + 'true'
      if actual.endswith('true'):
        await message.channel.send('You have already logged in before.')
        return
      if actual != password:
        await message.channel.send('Wrong password!')
    if (author in keys) == False:
      await message.channel.send('No account registered. Register using `$signup (password)`')
    return

  elif message.content.startswith('$logout') or message.content.startswith('$lo'):
    if 'true'in db[author]:
      db[author] = db[author][:-4]
      await message.channel.send('Logged out.')
    else:
      await message.channel.send('You have logged out before.')
    return
  



  
  
  
  
  elif message.content.startswith('$add'):
    guild_id = db[message.guild.id]
    if (author in keys) == True:
      check = db[author]
      if check.endswith('true'):
        id = message.guild.id
        guild = message.guild
        await message.channel.send('adding note for' + ' ' + '`' + str(guild) + '`.....')
        index = 0
        results = []
        while index < len (guild_id):
          index = guild_id.find('•', index)
          if index == -1:
            break
          results.append(index)
          index += 1
        point = message.content[4:]
        valu = db[id] 
        db[id] = valu + str(len(results)+ 1) + '•' + ' ' + point + '''
        '''
        embedVar = discord.Embed( title = 'Notes for' + ' ' + str(guild)  ,description = db[id], color=0x00ff00)
        await message.channel.send(embed = embedVar)
      else:
        await message.channel.send('Please login or signup first using `$signup (password)` or `$login (password)` ')
    return
  
  elif message.content.startswith('$clear') or message.content.startswith('$cls'):
    check = db[author]
    if check.endswith('true'):
      db[message.guild.id] = ''
      await message.channel.send('Notepad cleared.')
    else:
      await message.channel.send('Please login or signup first using `$signup (password)` or `$login (password)` ')
    return

  elif message.content.startswith('$pass'):
    await message.channel.send(db[author])
    return

  elif message.content.startswith('$notepad') or message.content.startswith('$np'):  
    check = db[author]
    if check.endswith('true'):
      guild_id = db[message.guild.id]
      index = 0
      results = []
      while index < len (guild_id):
        index = guild_id.find('•', index)
        if index == -1:
          break
        results.append(index)
        index += 1
      id = message.guild.id
      for position in results:
        db[id] = guild_id[:position-1] + str(results.index(position)+1) + guild_id[position:]
      guild = message.guild
      embedVar = discord.Embed( title = 'Notes for' + ' ' + str(guild) ,description = db[id], color=0x00ff00)
      await message.channel.send(embed = embedVar)
    else:
      await message.channel.send('Please login or signup first using `$signup (password)` or `$login (password)` ')
    return  

  elif message.content.startswith('$remove'):
    check = db[author]
    if check.endswith('true'):  
      guild = message.guild
      target = int(message.content[8:]) - 1
      guild_id = db[guild.id]
      index = 0
      results = []
      while index < len (guild_id):
        index = guild_id.find('•', index)
        if index == -1:
          break
        results.append(index)
        index += 1
      print(results[target])
      if target == -1:
        after= guild_id[results[target+1]:]
        db[guild.id] = after
      elif target == len(results) -1 :
        before = guild_id[:(results[target]-1)]
        db[guild.id] = before
      else:
        before = guild_id[:(results[target]-1) ]
        after= guild_id[results[target+1]:]
        db[guild.id] = before + after
      await message.channel.send('Entity removed.')
      id = message.guild.id
      guild = message.guild
      guild_id = db[message.guild.id]
      index = 0
      results = []
      while index < len (guild_id):
        index = guild_id.find('•', index)
        if index == -1:
          break
        results.append(index)
        index += 1
      for position in results:
        db[id] = guild_id[:position-1] + str(results.index(position)+1) + guild_id[position:]
      embedVar = discord.Embed( title = 'Notes for' + ' ' + str(guild) ,description = db[id], color=0x00ff00)
      await message.channel.send(embed = embedVar)
    else:
      await message.channel.send('Please login or signup first using `$signup (password)` or `$login (password)` ')
    return 

  
  elif message.content.startswith('$help'):
    embedVar = discord.Embed(title="Hello there.", description=
    '''Welcome to Tha Notepad Boi, this is a organisational bot that has the following commands:
    `$notepad` or `$np` : get the shared notepad for the server in which you are.
    `$add`: Add a note to the notepad for it to be visible to all.
    `$cls` or `$clear` :  Clear all notes in the notepad.
    `$remove (index)`: Remove an item at prescribed index.

    **Important** For you to be able to add notes, you should also be logged in, use `$login (password)` or `$signup (password)` if you are not signed up yet.
    Authorizational commands:
    `$login (password)`: login to access the bot
    `$signup (password)`: signup first if you are not registered.
    `$logout`: log out.
    Aaand thats it! ''',
    color=0x00ff00)
    await message.channel.send(embed=embedVar)
  #after this bot was rarely used, i started using it for myself, namely getting books from libgen.is
  elif message.content.startswith('$book'):
    s = message.content.split(' ',2)
    title = s[2].replace(' ', '+')
    format = s[1]
    req = requests.get(f"https://libgen.is/search.php?req={title}&res=100")   .text
    soup = BeautifulSoup( req , 'lxml')
    article = soup.find_all('tr')
    article = article[2:-1]
    for i in article:
        s= i.find_all('td')
        if s[8].text == format:
            await message.channel.send(str(s[11]).split('"')[1])
            await message.channel.send(s[2].text)
            break
    else:
        if len(article) > 2:
            await message.channel.send('Available in other formats such as')
            l = []
            for i in article[1:]:
                s= i.find_all('td')
                if s[8].text not in l :
                    await message.channel.send(s[8].text)
                    l.append(s[8].text)
        else:
          await message.channel.send('Unable to find book')
  elif message.content.startswith('.test'):
    embed = discord.Embed(title = 'Test!',colour = discord.Color.dark_gold(),description = 'This and [That](https://replit.com/@AdvaithGS/Notepad-boi#main.py)')
    file = discord.File('test.jpg')
    embed.set_image(url = 'attachment://test.jpg')
    embed.set_footer(text = 'Im just trying to see how images can be added to embeds in a different way.')
    await ctx.send(embed=embed, file=file)  
  
  

keep_alive()
client.run('ODA4MjYyODAzMjI3NDEwNDY1.YCD_ZQ.EDL3Sg03X1VU6zk2sqEyMtA-JPQ')# lmao use this
#dark blue,
