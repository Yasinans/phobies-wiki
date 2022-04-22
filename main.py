from discord.ext import commands

bot = commands.Bot(command_prefix = "!")
bot.load_extension("Wiki")

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    
bot.run("OTU1MzIwNTUwMjcwNTc0NjQ0.Yjf9mA.qlbPAIgVPjiJ7NB0nvzcprVMA_o")
