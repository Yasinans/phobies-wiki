#from urllib.request import urlopen
from discord.ext import commands
from discord.ui import Modal, InputText
import requests
import discord
import random
import time
#import threading
import asyncio
import validators
import datetime
import pytz

#blah blah setup
image_formats = ("image/png", "image/jpeg", "image/gif")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
ongoing = []
bot.remove_command('help')

#cog?
guild_ids = [952985390124507216, 930177578004791356]
Date = ""
Incoming = ""
Staying = ""
GoingOut = ""
PacificTime = ""

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False
#commands slash

@bot.slash_command(guild_ids=guild_ids, description="List all the commands")
async def help(ctx):
    embed=discord.Embed(color=0x3D550C)
    embed.add_field(name="Command List:\n", value="**/phobie (Phobie Name)** - Search for the information of a Phobie.\n**?report bug** - Report a bug you encounter in the game.\n**?suggest** - Make a suggestion that you want to see in the game, on the website/forums, or in the Discord Server", inline=False)
    await ctx.respond(embeds=[embed], ephemeral=True)

class mapModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Date (Format: Month Day, Year)", placeholder="Date"))
        self.add_item(InputText(label="Incoming Maps (Example: Map1, Map2)", placeholder="map1"))
        self.add_item(InputText(label="Staying Maps (Example: Map1, Map2)", placeholder="map2"))
        self.add_item(InputText(label="Going Out (Example: Map1, Map2)", placeholder="map3"))
    async def callback(self, interaction: discord.Interaction):
        global Date
        global Incoming
        global Staying
        global GoingOut
        global PacificTime
        #replace each , with a new line in the string
        Date = self.children[0].value
        Incoming = self.children[1].value.replace(",", "\n")
        Staying = self.children[2].value.replace(",", "\n")
        GoingOut = self.children[3].value.replace(",", "\n")
        pacific = pytz.timezone('US/Pacific')
        PacificTime = datetime.datetime.now(pacific).strftime("%Y-%m-%d %H:%M:%S")

        await interaction.response.send_message("Map Rotation Updated!", ephemeral=True)

@bot.slash_command(guild_ids=guild_ids, description="Update the description of the map rotation")
@commands.has_permissions(manage_messages=True)
async def updatemap(ctx):
    modal = mapModal(title="Update Map Rotation")
    await ctx.send_modal(modal)
@bot.slash_command(guild_ids=guild_ids, description="Get the current map rotation")
async def maprotation(ctx):
    global Date
    global Incoming
    global Staying
    global GoingOut
    embed=discord.Embed(title="WEEKLY MAP ROTATION", description="Date: "+Date,color=0x3D550C)
    embed.add_field(name="Incoming Maps: ", value=Incoming, inline=True)
    embed.add_field(name="Staying Maps:", value=Staying, inline=True)
    embed.add_field(name="Going Out:", value=GoingOut, inline=True)
    embed.set_footer(text="Last Updated: " + PacificTime + " PST")
    await ctx.respond(embeds=[embed], ephemeral=True)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def broadcastmap(ctx):
    global Date
    global Incoming
    global Staying
    global GoingOut
    embed=discord.Embed(title="WEEKLY MAP ROTATION", description="Date: "+Date,color=0x3D550C)
    embed.add_field(name="Incoming Maps: ", value=Incoming, inline=True)
    embed.add_field(name="Staying Maps:", value=Staying, inline=True)
    embed.add_field(name="Going Out:", value=GoingOut, inline=True)
    embed.set_footer(text="Last Updated: " + PacificTime + " PST")
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    bot.loop.create_task(status_task())

async def status_task():
    phobieguild = bot.get_guild(930177578004791356)
    while True:
        await bot.change_presence(activity=discord.Game(name="Phobies"))

        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{len([m for m in phobieguild.members if not m.bot])} Wranglers'),
            status=discord.Status.online)
        await asyncio.sleep(1800)
        
#prefix
@bot.group()
async def report(ctx):
    #initiate
    if ctx.invoked_subcommand is None:
        return await ctx.send('Do "?report bug" to report a bug, Do "?suggest" to suggest a feature.')


@report.command(name='bug')
async def _report(ctx):
    if ctx.message.author.id in ongoing:
        await ctx.message.reply("You still have ongoing request! Make sure to complete it or wait for it to expire", delete_after=5)
        return
    else: ongoing.append(ctx.message.author.id)
    author = ctx.message.author
    await ctx.message.reply(f"**Hi {author.name}, please check your messages so we can assist you in your report.**", delete_after=5)
    #direct Message
    try:
        await ctx.message.author.send(f"Thank you {ctx.message.author.name}  for your report! Kindly answer the following questions asked to you with the details of your report. Make sure to prepare and provide evidence such a screenshot or recorded video clip of the issue if possible. *Type ?stop to cancel ongoing request.* \n\n**NOTES:** We will never ask you for any personal information, official documents, or receipts on Discord. We will also never ask you to share your account's recovery code with us. For account and payment related issues, please contact community@smokingguninc.com properly stating your issue.\n\nLet us begin.\n\n")
    except:
        await ctx.message.reply("It seems like I can't send a direct message to you. Please check your Privacy or Direct Messages Settings", delete_after=10)
        ongoing.remove(ctx.message.author.id)
        return
    questions = ["What is your Phobies In-Game Name?", "What priority level do you think should the report be given?\n\n1 - Low\n2 = Medium\n3 = High", "What device model are you playing the game on?", "What Operating System and version are you using?", "Please describe the issue. Note: Maximum of 1000 characters only", "Please send evidence by attaching a screenshot or a valid video/image link. Put N/A if none"]
    #checking
    def priority(pnum):
        pnum = int(pnum)
        if pnum == 1: return "https://media.discordapp.net/attachments/952985390577492005/953951134245081088/Yellow_Circle.png?width=475&height=475"
        elif pnum == 2: return "https://cdn.discordapp.com/attachments/952985390577492005/953950220197171271/Orange_Circle.png"
        elif pnum == 3: return "https://cdn.discordapp.com/attachments/952985390577492005/953951134035370004/Red_Circle.png"
    def check(msg):
        if ctx.message.author.id not in ongoing:
            raise ValueError("Cancelled command")
        try:
            return len(msg.content) <= 10000 and len(msg.content) >= 1 and msg.author == author and not msg.guild
        except:
            return False;
    def check_valid(msg):
        if ctx.message.author.id not in ongoing:
            raise ValueError("Cancelled command")
        try:
            if  msg.content.lower() == "n/a": return True
            elif msg.attachments[0].url: return True
            elif validators.url(msg.content):
                return len(msg.content) <= 300 and len(msg.content) >= 1 and msg.author == author and not msg.guild
            else: return False;
        except Exception as e:
            return False;

    def check_priority(msg):
        if ctx.message.author.id not in ongoing:
            raise ValueError("Cancelled command")
        try:
            #print(msg.content.lower())
            priorities = int(msg.content)
            if msg.content.isdigit(): return priorities <= 3 and priorities >= 1
            else: return False
        except:
            return False
    #loop
    data = []
    i = 0
    while i < 6:
        try:
            if ctx.message.author.id not in ongoing:
                return
            await ctx.message.author.send(questions[i])
            if i == 5:
                msg = await bot.wait_for("message", check=check_valid, timeout=360) # 30 seconds to reply
                if msg.attachments:
                    data.append(msg.attachments[0].url)
                else:
                    data.append(msg.content)
                i += 1
            elif i == 1:
                msg = await bot.wait_for("message", check=check_priority, timeout=360) # 30 seconds to reply
                data.append(msg.content)
                i += 1
            else:
                msg = await bot.wait_for("message", check=check, timeout=360) # 30 seconds to reply
                data.append(msg.content)
                i += 1
            #print(i)
        except asyncio.TimeoutError:
            await ctx.message.author.send("You took too long, please submit your report again!")
            ongoing.remove(ctx.message.author.id)
            return
    await ctx.message.author.send("Thank you for submitting your report.")
    #print(data)
    ongoing.remove(ctx.message.author.id)
    #embed
    embed=discord.Embed(color=0xd52020)
    embed.set_thumbnail(url=str(priority(data[1])))
    if author.avatar.url is None: embed.set_author(name= "Bug Report From " + author.name + "")
    else: embed.set_author(name= "Bug Report From " + author.name + "", icon_url=author.avatar.url)
    embed.add_field(name="IGN", value=data[0], inline=True)
    embed.add_field(name="Device Model", value=data[2], inline=True)
    embed.add_field(name="Operating System", value=data[3], inline=True)
    embed.add_field(name="Description", value=data[4], inline=False)
    try:
        if is_url_image(data[5]) :  # check if the content-type is a image
            embed.set_image(url = data[5])
        else:
            embed.add_field(name="Link of proofs", value=str(data[5]), inline=False)
    except:
        embed.add_field(name="Link of proofs", value=str(data[5]), inline=False)
    sendembed = await bot.get_channel(953708921183432714).send(embed=embed)
    
@bot.command()
@commands.dm_only()
async def stop(ctx):
    if ctx.message.author.id in ongoing:
        await ctx.message.reply("Your current request is now stopped. You can now create another one")
        ongoing.remove(ctx.message.author.id)
    else:
        await ctx.message.reply("You don't have ongoing request!")
    return
@bot.command(aliases=['suggestion'])
async def suggest(ctx):
    if ctx.message.author.id in ongoing:
        await ctx.message.reply("You still have ongoing request! Make sure to complete it or wait for it to expire", delete_after=5)
        return
    else: ongoing.append(ctx.message.author.id)
    author = ctx.message.author
    await ctx.message.reply(f"**Hi {author.name}, please check your messages so we can assist you in your suggestion.**", delete_after=5)
    await ctx.message.delete()
    #direct Message
    try:
        await ctx.message.author.send(f"Thank you {ctx.message.author.name}  for your suggestion! Kindly answer the following questions asked to you with the details of your suggestion.\n\nLet us begin. *Type ?stop to cancel ongoing request*")
    except:
        await ctx.message.reply("It seems like I can't send a direct message to you. Please check your Privacy or Direct Messages Settings", delete_after=10)
        ongoing.remove(ctx.message.author.id)
        return
    questions = ["What is the title of your suggestion?", "What type of suggestion are you making?\n\n1 - Discord Server\n2 - Website/Forums\n3 - Game\n4 - Others", "What is the description of your suggestion? Note: Maximum of 1000 characters only"]
    #checking
    def cats(catnum):
        catnum = int(catnum)
        if catnum == 1: return "Discord Server"
        elif catnum == 2: return "Website/Forums"
        elif catnum == 3: return "Game"
        elif catnum == 3: return "Others"
    def check(msg):
        if ctx.message.author.id not in ongoing:
            raise ValueError("Cancelled command")
        try:
            return len(msg.content) <= 10000 and len(msg.content) >= 1 and msg.author == author and not msg.guild
        except:
            return False;
    def check_type(msg):
        if ctx.message.author.id not in ongoing:
            raise ValueError("Cancelled command")
        try:
            typecat = int(msg.content)
            if msg.content.isdigit(): return typecat <= 4 and typecat >= 1 
            else: return False
        except:
            return False
    #loop
    data = []
    i = 0
    while i < 3:
        try:
            if ctx.message.author.id not in ongoing:
                return
            await ctx.message.author.send(questions[i])
            if i == 1:
                msg = await bot.wait_for("message", check=check_type, timeout=360) # 30 seconds to reply
                data.append(msg.content)
            else:
                msg = await bot.wait_for("message", check=check, timeout=360) # 30 seconds to reply
                data.append(msg.content)
            i += 1
        except asyncio.TimeoutError:
            await ctx.message.author.send("You took too long, please submit your suggestion again!")
            ongoing.remove(ctx.message.author.id)
            return
    await ctx.message.author.send("Thank you for submitting your suggestion.")
    #print(data)
    ongoing.remove(ctx.message.author.id)
    #embed
    embed=discord.Embed(color=0xFFFF00)
    if author.display_avatar: embed.set_thumbnail(url=author.display_avatar)
    if author.display_avatar is None: embed.set_author(name= "Suggestion From " + author.name + "")
    else: embed.set_author(name= "Suggestion From " + author.name + "", icon_url=author.display_avatar)
    embed.add_field(name="Title", value=data[0], inline=True)
    embed.add_field(name="Category", value=str(cats(data[1])), inline=True)
    embed.add_field(name="Suggestion Description", value=data[2], inline=False)


    sendembed = await bot.get_channel(953708921762246667).send(embed=embed)
    await sendembed.add_reaction("👍")
    await sendembed.add_reaction("👎")
@bot.command()
@commands.has_permissions(manage_messages=True)
async def rafflecancel(ctx):
    ongoing.remove(ctx.message.author.id)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def reroll(ctx, messageid: int, answer: str):
    winners = []
    channel = 952985390392959099
    channels = bot.get_channel(952985390392959099)
    theembed = await channels.fetch_message(messageid) 
    if answer == "A":
        print(datas[4])
        for reaction in theembed.reactions:
            if reaction.emoji == "🇦":
                async for user in reaction.users():
                    winners.append(user)
            print(reaction.emoji)
    elif answer == "B":
        for reaction in theembed.reactions:
                if reaction.emoji == "🇧":
                    async for user in reaction.users():
                        winners.append(user)
    elif answer == "C":
            for reaction in theembed.reactions:
                if reaction.emoji == "🇨":
                    async for user in reaction.users():
                        winners.append(user)
    elif answer == "D":
        for reaction in theembed.reactions:
            if reaction.emoji == "🇩":
                async for user in reaction.users():
                    winners.append(user)
    winners.remove(bot.user)
    if len(winners) == 0:
        await ctx.message.reply("No one won!")
        return
    winner = random.choice(winners)
    await bot.get_channel(channel).send("Rerolling..... The new winner is **<@" + str(winner.id) + ">**!")
@bot.command()
@commands.has_permissions(manage_messages=True)
async def raffle(ctx):
    author = ctx.message.author
    channel = 952985390392959099
    channels = bot.get_channel(952985390392959099)
    datas = []
    if ctx.message.author.id in ongoing:
        await ctx.message.reply("You still have ongoing request! Type ?rafflecancel to cancel", delete_after=5)
        return
    else: ongoing.append(ctx.message.author.id)
    questions = ["What is the question for raffle?","What is the answer for A.?","What is the answer for B.?","What is the answer for C.?","What is the real answer? Type the letter of the answer. Ex: \"A\""]
    def check(msg):
        return msg.author == author
    def checks(msg):
        return msg.content == "A" or msg.content == "B" or msg.content == "C" or msg.content == "D"
    i = 0
    while i < 5:
        try:
            await ctx.message.reply(questions[i])
            if i == 4:
                msg = await bot.wait_for("message", check=checks, timeout=130) # 30 seconds to reply
                datas.append(msg.content)
            else:
                msg = await bot.wait_for("message", check=check, timeout=130) # 30 seconds to reply
                datas.append(msg.content)
            i += 1
        except asyncio.TimeoutError:
            await ctx.message.reply("You took too long")
            ongoing.remove(ctx.message.author.id)
            return
    await ctx.message.reply("Done. It's starting now!")
    ongoing.remove(ctx.message.author.id)
    embed=discord.Embed(title=datas[0], description="Click on the letter corresponding to the correct answer and one person will randomly win 500 Coffee Beans!", color=0xff9238)
    embed.add_field(name=f":regional_indicator_a: {datas[1]}", value='\u200b', inline=True)
    embed.add_field(name=f":regional_indicator_b: {datas[2]}", value='\u200b', inline=False)
    embed.add_field(name=f":regional_indicator_c: {datas[3]}", value='\u200b', inline=False)
    embed.set_footer(text=f"Hosted By: {author.name}")
    sends = await bot.get_channel(channel).send(embed=embed)
    await sends.add_reaction("🇦")
    await sends.add_reaction("🇧")
    await sends.add_reaction("🇨")
    await bot.get_channel(channel).send("15 minutes left!")
    await asyncio.sleep(600)
    await bot.get_channel(channel).send("5 minutes left!")
    await asyncio.sleep(240)
    await bot.get_channel(channel).send("1 minute left!")
    await asyncio.sleep(60)
    winners = []
    theembed = await channels.fetch_message(sends.id) 
    if datas[4] == "A":
        print(datas[4])
        for reaction in theembed.reactions:
            if reaction.emoji == "🇦":
                async for user in reaction.users():
                    winners.append(user)
            print(reaction.emoji)
    elif datas[4] == "B":
        for reaction in theembed.reactions:
                if reaction.emoji == "🇧":
                    async for user in reaction.users():
                        winners.append(user)
    elif datas[4] == "C":
            for reaction in theembed.reactions:
                if reaction.emoji == "🇨":
                    async for user in reaction.users():
                        winners.append(user)
    elif datas[4] == "D":
        for reaction in theembed.reactions:
            if reaction.emoji == "🇩":
                async for user in reaction.users():
                    winners.append(user)
    winners.remove(bot.user)
    if len(winners) == 0:
        await ctx.message.reply("No one won! Try again!")
        return
    winner = random.choice(winners)
    await bot.get_channel(channel).send("Times up! The correct answer is **" + datas[4] + "**. The winner is **<@" + str(winner.id) + ">**!")

bot.load_extension("wiki")
bot.run('')
