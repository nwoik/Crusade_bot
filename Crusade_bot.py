import discord
from discord.ext import commands
from itertools import cycle
import random
import json
import os
import time
import datetime
import asyncio

client = commands.Bot(command_prefix = "$")

boomer_emotes = [":peteranderson:", ":goobleglurg:"]

shadow_muted = []

polls = []


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Crusade of the Analog lands"))
    print("Hello there")


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if ("general" in str(channel) and not "old" in str(channel)):
            await channel.send("""Welcome to the server %s""" % member.mention)
            print("""Welcome to the server %s""" % member.mention)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == client.user:
        message = reaction.message   
        for e in message.reactions:
            if e.me == False:
                await e.remove(user)

@client.event
async def on_message(message):
    if type(message.channel) == discord.DMChannel:
        print("(%s : %s): %s\n%s" % (message.author.name, message.author.mention, message.content, message.attachments))
        BOT_DMS = await client.fetch_channel(857214111540314142)
        await BOT_DMS.send("%s: %s\n%s" % (message.author.mention, message.content, message.attachments))

    if message.author == client.user:
        return

    if message.author in shadow_muted:
        await message.channel.purge(limit = 1)

    if "slime" in message.content.lower().strip(" "):
        await message.channel.send("https://media.discordapp.net/attachments/728599009261781052/749299359946113164/Sprite-0001.gif")

    if message.content.lower() == "mage":
        await message.channel.send("https://cdn.discordapp.com/attachments/728599009261781052/763876231824932874/Cloak.gif")

    if "nigga" in message.content.lower().strip(" "):
        shadow_muted.append(message.author)
        await message.channel.send("https://tenor.com/view/youremuted-gif-20283179")
    
    # await message.channel.send(message.author.mention + " " + str(message.content))

    await client.process_commands(message)


@client.command()
async def ping(context):
    await context.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=1):
    await context.channel.purge(limit = amount+1)


@client.command()
@commands.has_permissions(manage_messages=True)
async def shadowmute(context, member : discord.Member):
    guild = context.guild
    shadow_muted.append(member)
    await context.send(member.mention + "\nhttps://tenor.com/view/youremuted-gif-20283179")
    print(shadow_muted)


@client.command()
@commands.has_permissions(manage_messages=True)
async def unshadowmute(context, member:discord.Member):
    if len(shadow_muted) != 0:
        shadow_muted.remove(member)
        await context.send(member.mention + " has been unmuted \nhttps://tenor.com/view/kars-unmuted-gif-19036031")
    print(shadow_muted)

@client.command()
async def gtfo_discord(context, time=1):
    time = time*3600
    shadow_muted.append(context.author)
    await asyncio.sleep(time)
    shadow_muted.remove(context.author)
    await context.send("%s \nhttps://tenor.com/view/connor-mc-gregor-gtfo-gtfoh-get-the-fuck-out-of-here-gif-10203692" % context.author.mention)


@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(context, member : discord.Member):
    await member.kick()
    await context.send("https://tenor.com/view/breakdance-kick-kid-gif-11600755")


@client.command()
@commands.has_permissions(manage_messages=True)
async def mass_kick(context, role : discord.Role, guild_name=""):
    for member in role.members:
        await context.guild.kick(member)
    await context.send("Everyone with the role %s has been excommunicated" % role)


@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(context, member : discord.Member, reason=None):
    await member.ban(reason=reason)
    await context.send("https://tenor.com/view/bane-no-banned-and-you-are-explode-gif-16047504")


@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(context, member):
    banned_ppl = await context.guild.bans()
    member_name, member_disc = member.split("#")
    for x in banned_ppl:
        user = x.user    
        if (user.name, user.discriminator) == (member_name, member_disc):
            await context.guild.unban(user)
            await context.send("%s has been absolved of his crimes" % (user))


@client.command()
async def member_count(context, server_name=""):
    guild = context.guild
    await context.send("""```ini\n[Total members: %s]\n```""" % context.guild.member_count)


@client.command()
@commands.has_permissions(manage_messages=True)
async def say(context, guild_name="", channel_name="", msg=""):
    for guild in client.guilds:
        if guild_name in str(guild).lower():     
            for channel in guild.channels:              
                if channel_name in str(channel):
                    await channel.send(msg)    


@client.command()
@commands.has_permissions(manage_messages=True)
async def guildinfo(context):
    guild = context.guild
    embed = discord.Embed(title="%s" % guild, description="Join The Crusade", timestamp=context.message.created_at, color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="**Owner:**", value=guild.owner,inline=False)
    embed.add_field(name="**Member Count:**", value=guild.member_count, inline=False)
    embed.add_field(name="**Role Count:**", value=len(guild.roles), inline=False)
    embed.add_field(name="**Booster Count:**", value=guild.premium_subscription_count, inline=False)
    embed.add_field(name="**Emoji Limit:**", value=guild.emoji_limit, inline=False)
    embed.add_field(name="**Server Created At:**", value=guild.created_at, inline=False)
    embed.set_footer(text="Requested by %s" % context.author, icon_url=context.author.avatar_url)
    await context.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def member_info(context):
    guild = context.guild
    embed = discord.Embed(title="%s" % guild, description="Member Info (Local)", timestamp=context.message.created_at, color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon_url)
    for role in guild.roles:
        embed.add_field(name=str(role.name), value=str(len(guild.get_role(role.id).members)), inline=False)
    embed.set_footer(text="Requested by %s" % context.author, icon_url=context.author.avatar_url)
    await context.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def role(context, member:discord.Member, rl):
    for r in context.guild.roles:
        if rl == r.name:
            rl = r
            print(r)
    await member.add_roles(r)
    await context.send(f"{member} has got the role {r}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def poll(context, statement="", choices="", duration=30):  
    numbers = {1:"1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣", 6:"6️⃣", 7:"7️⃣", 8:"8️⃣", 9:"9️⃣"}
    opt_dict = {}
    choices = choices.split("/")
    options = ""
    guild = context.guild
    embed = discord.Embed(title="%s" % statement, description="Drop your vote in the poll", timestamp=context.message.created_at, color=discord.Color.red())
    embed.set_thumbnail(url=guild.icon_url)
    for x in range(0, len(choices)):
        options += "%s %s \n" % (numbers[x+1], choices[x])
        opt_dict[numbers[x+1]] = choices[x]
    embed.add_field(name="**Options**", value="%s" % options, inline=False)
    embed.add_field(name="**Instructions**", value="React to cast a vote", inline=False)
    embed.set_footer(text="Requested by %s" % context.author, icon_url=context.author.avatar_url)
    await context.send("Cast your vote in the poll")
    message = await context.send(embed=embed)
    message_id = message.id
    print(opt_dict)
    for x in list(numbers.values()):
        if x in options:
            await message.add_reaction(x)
    
    await asyncio.sleep(duration)
    async for msg in context.channel.history(limit=100):
        if msg.id == message_id:
            message = msg
    y = 0
    print(message.reactions)
    for x in message.reactions:
        print(x.count)
        if x.count > y and x.emoji in opt_dict:
            y = x.count
            res = x.emoji
    print(res)
    end = ("Most of you voted %s" % opt_dict[res])
    await message.channel.send(end)


@client.command()
@commands.has_permissions(manage_messages=True)
async def react(context, message_id, emoji):
    message = await context.channel.fetch_message(int(message_id))
    await message.add_reaction(emoji)


@client.command()
@commands.has_permissions(manage_messages=True)
async def DM(context, user:discord.User, msg):
    await user.send(msg)
    print(msg)
    return

def flip(list1, call=""):
    x = random.randint(0,1)
    if call != "" and call in list1:
        if list1[x] == call:
            call = "right"
        else:
            call = "wrong"
        return "You got %s, you guessed %s" % (list1[x], call)
    else:
        return "You got %s" % list1[x]


@client.command()
async def coin(context, call=""):
    toss = flip(["heads", "tails"], call)
    await context.send(toss)

@client.command()
async def servers(context):
    embed = discord.Embed(title="Servers I'm operating in", description="", timestamp=context.message.created_at, color=discord.Color.gold())
    embed.set_thumbnail(url=client.user.avatar_url)
    output = ""
    x = 0
    for guild in client.guilds:
        x += 1
        output += "%d. %s \n" % (x, guild)
    embed.add_field(name="**Servers:**", value="%s" % output, inline=True)
    embed.set_footer(text="Requested by %s" % context.author, icon_url=context.author.avatar_url)
    await context.send(embed=embed)

@client.command()
async def Gucci(context):
    await context.send("sup fellas! how r we all?")
    
my_key = os.environ["MY_KEY"]
client.run(my_key)
