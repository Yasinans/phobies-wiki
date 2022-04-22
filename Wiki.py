import xlrd
import discord
from difflib import get_close_matches
from discord.ext import commands

class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client
	
    @commands.command()
    async def phobie(self, ctx, phobie: str):
        result = search(phobie)
        if isinstance(result, list):
            #send discord embed, on construction 
            embed=discord.Embed(title="[:key_emoji: 6] Phobie Name: " + result[1], description="Description of Phobie", color=0x532caf)
            embed.set_footer(text="Phobies Wiki")
            await ctx.send(embed=embed)
        else:
	        await ctx.send(result)


def setup(bot):
    bot.add_cog(Wiki(bot))
    


#parsing

loc = ("verified.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

def search(Phobie):
    currentdata = []
    rows = 0
    
    for r in range(sheet.nrows):
        cell = sheet.cell(r, 1)
        if str(cell.value).lower() == str(Phobie).lower():
            rows = r
        currentdata.append(str(cell.value).lower())
    if rows == 0:
        closewords = get_close_matches(Phobie.lower(), currentdata,cutoff=0.5)
        result = "Did you mean: "
        for close in closewords:
            #Uppercase the first character of the word in the variable close
            close = close[0].upper() + close[1:]
            if len(closewords) == 1:
                result += close
            else: result += close + ", "
        return result
    else:
        result = sheet.row_values(rows)
        return result