from discord.ext import commands

bot = commands.Bot(command_prefix = "!")
bot.load_extension("Wiki")

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    
bot.run("token")
