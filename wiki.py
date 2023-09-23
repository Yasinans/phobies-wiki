from pip import main
from bs4 import BeautifulSoup
from difflib import get_close_matches
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import slash_command, Option

import discord
import requests
import asyncio

guild_ids = [930177578004791356]
phobielist = []
phobieP1 = {
    "Key": 0,
    "Stress Level": 0,
    "Race": "",
    "Icon": "",
    "Rarity": "",
    "Health": 0,
    "Movement Range": 0,
    "Movement Type": "",
    "Attack Range": 0,
    "Attack Type": "",
    "Attack Damage": 0,
    "Fire Damage": 0,
    "Electric Damage": 0,
    "Poison Damage": 0,
    "Effect Range": "",
    "Rarity": "",

}
phobieP2 = {
    "Description": "",
    "HP Lifesteal": "",
    "Attack Reflect": "",
    "Attack Damage": 0,
    "Electric Reflect": "",
    "Effect Range": "",
    "Effect Duration": 0,
    "HP Heal": "",
    "Health": 0,
    "Additional Movement": 0,
    "Damage Buff": "",
    "Disease Damage": ""
}
phobieP3 = {
    "Description": "",
    "Attack Range": "",
    "Attack Damage": 0,
    "Additional Movement": 0,
    "HP Heal": "",
    "Lifesteal": "",
    "Obstacle HP": 0,
    "Damage Buff": "",
    "Damage Debuff": "",
    "Trap Damage": 0,
    "Attack Type": "",
    "Electric Damage": 0,
    "Poison Damage": "",
    "Fire Damage": "",
    "Disease Damage": "",
    "Effect Duration": 0,
    "Effect Range": "",
    "Effect Duration": 0,
    "Cooldown": 0,
    "Unlocking": 0,
    "Movement Range": 0,
}


class wiki(commands.Cog):
    def __init__(self, client):
        self.client = client
        getList()

    @slash_command(guild_ids=guild_ids, description="Search Phobie")
    async def phobies(self, ctx: commands.Context, *, name: Option(str, "Enter the name of the Phobie you want to search for", required=True)):
        try :
            embeds = parseTable(get_close_matches(name, phobielist)[0])
        except :
            closewords = get_close_matches(name, phobielist, cutoff=0.5)
            strings = "No results found. "
            if len(closewords) > 0:
                strings += " Did you mean: "
                for close in closewords:
                    # Uppercase the first character of each word in the variable close
                    close = close.title()

                    if len(closewords) == 1:
                        strings += close
                    else:
                        strings += close + ", "
            await ctx.respond(strings, ephemeral=True)
            return

        embed = embeds[0]
        i = 0
        embed.set_footer(text=f"Page 1/Page {len(embeds)} - Phobies Wiki Team - Note: Let us know if you discovered any error.")
        btn1 = Button(
            label="",
            emoji="⏪",
            row=0,
            disabled=True
        )
        btn2 = Button(
            label="",
            emoji="⏩",
            row=0,
        )
        view = View(disable_on_timeout=True)
        view.add_item(btn1)
        view.add_item(btn2)

        async def button1(interaction: discord.Interaction):
            wario = await left(i)
            if(i == 0):
                btn1.disabled = True
            else:
                btn1.disabled = False
            btn2.disabled = False
            currentembed = embeds[wario]
            currentembed.set_footer(
                text=f"Page {wario+1}/{len(embeds)} - Phobies Wiki Team - Note: Let us know if you discovered any error.")
            await interaction.response.edit_message(embed=currentembed, view=view)
            

        async def button2(interaction: discord.Interaction):
            wario = await right(i)
            if(i == len(embeds)-1):
                btn2.disabled = True
            else:
                btn2.disabled = False
            btn1.disabled = False
            currentembed = embeds[wario]
            currentembed.set_footer(
                text=f"Page {wario+1}/{len(embeds)} - Phobies Wiki Team - Note: Let us know if you discovered any error.")
            await interaction.response.edit_message(embed=currentembed, view=view)
        btn1.callback = button1
        btn2.callback = button2

        async def right(a):
            if a < len(embeds)-1:
                nonlocal i
                i = a + 1
                return i
            else:
                return i

        async def left(a):
            nonlocal i
            i = a
            if a > 0:
                i = a - 1
                return i
            else:
                return i
        await ctx.respond(embed=embed, view=view, ephemeral=True)

    @slash_command(guild_ids=guild_ids, description="Penk")
    async def test(self, ctx: commands.Context):
        print(phobielist)


def getList():
    URL = "https://phobies.fandom.com/wiki/Category:Phobies"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    phCat = soup.find('div', attrs={'class': 'category-page__members'})
    for row in phCat.findAll('a', attrs={'class': 'category-page__member-link'}):
        if "User:" not in str(row.text):
            phobielist.append(row.text)


def parseTable(phobie):
    URL = "https://phobies.fandom.com/wiki/" + phobie
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    # First Table
    baseTable = soup.find('table', attrs={'style': 'width:430px'})
    baseDescription = soup.find('span', attrs={'style': 'font-size:16px;'})
    baseUrl = soup.find(
        'span', attrs={'style': 'text-shadow:-3px 3px 3px black;'})
    # if baseDescription is none, then make the description "No Description available"
    secondTables = soup.find_all('table', attrs={
        'style': 'background:#464B60; border:1px solid #282B38; border-radius: 10px 10px 0px 0px; padding:10px; margin-bottom:0px; font-size: 160%; width: 100%; text-align: left;'})
    secondData = soup.find_all('table', attrs={
        'style': 'background:#282B38; border:1px solid #282B38; border-radius: 0px 0px 10px 10px; padding:10px; margin-bottom:10px; font-size: 100%; width: 100%; text-align: left;'})

    if len(baseDescription.findAll('i')[0].text) < 3:
        pageOne = embedBuilder(baseTable.findAll(
            'tr'), 1, phobie, "No description available", baseUrl.findAll('img')[0]['src'])
        if len(secondTables) >= 2:
            pageTwo = embedBuilder(secondData[0].findAll(
                'tr'), 2, phobie, secondTables[0].findAll('b')[0].text, baseUrl.findAll('img')[0]['src'])
            if "Special Ability" in secondTables[1].findAll('b')[0].text:
                pageThree = embedBuilder(secondData[1].findAll(
                    'tr'), 3, phobie, secondTables[1].findAll('b')[0].text, baseUrl.findAll('img')[0]['src'])
            else:
                pageThree = embedBuilder(secondData[1].findAll(
                    'tr'), 2, phobie, secondTables[1].findAll('b')[0].text, baseUrl.findAll('img')[0]['src'])
            return [pageOne, pageTwo, pageThree]
        else:
            if "Special Ability" in secondTables[0].findAll('b')[0].text:
                pageTwo = embedBuilder(secondData[0].findAll(
                    'tr'), 3, phobie, secondTables[0].findAll('b')[0].text, baseUrl.findAll('img')[0]['src'])
            else:
                pageTwo = embedBuilder(secondData[0].findAll(
                    'tr'), 2, phobie, secondTables[0].findAll('b')[0].text, baseUrl.findAll('img')[0]['src'])
            return [pageOne, pageTwo]
    else:
        pageOne = embedBuilder(baseTable.findAll(
            'tr'), 1, phobie, baseDescription.findAll('i')[0].text, baseUrl.findAll('img')[0]['src'])
        return [pageOne]
    # for row in baseTable.findAll('tr'):
    #    print(row.findAll('td')[0].b.text + " " + row.findAll('td')[1].text)


def emojiFinder(name, type):
    if type == "attack":
        if name.lower() == "line of sight":
            emoji = "<:icon_range_line_of_sight:967647460883316736>"
        elif name.lower() == "lob":
            emoji = "<:icon_range_lob:967647464800813056>"
        elif name.lower() == "self-initiated aoe":
            emoji = "<:icon_aoe:967647458324774922>"
        elif name.lower() == "targeted aoe":
            emoji = "<:icon_aoe_targeted:967647458320580668>"
        elif name.lower() == "all map":
            emoji = "<:icon_aoe:967647458324774922>"
        else:
            emoji = "<:icon_range_line_of_sight:967647460883316736>"
    elif type == "movement":
        if name.lower() == "walking":
            emoji = "<:icon_movement_walk:967647464796594266>"
        elif name.lower() == "flying":
            emoji = "<:icon_movement_fly:967647461080449104>"
        elif name.lower() == "bypassing":
            emoji = "<:icon_movement_bypass:967647460631646289>"
    elif type == "effect":
        if name.lower() == "single target attack":
            emoji = "<:icon_damage:967647459587285052>"
        elif name.lower() == "targeted aoe attack":
            emoji = "<:icon_damage_AOE:967647459872497695> "
        elif name.lower() == "beam attack":
            emoji = "<:icon_damage_AOE_Line_Attack:967647460644233267>"
        elif name.lower() == "splash aoe attack":
            emoji = "<:icon_damage_AOE_Double:967647460665217034>"
        elif name.lower() == "dash attack":
            emoji = "<:icon_damage_Dash:967647463517335572>"
        elif name.lower() == "all map":
            emoji = "<:icon_aoe:967647458324774922>"
        else:
            emoji = "<:icon_damage:967647459587285052>"
    return emoji


def embedBuilder(data, page, name, descriptions, url):
    if page == 1:
        pP1 = phobieP1.copy()
        for i in range(0, 13):
            # check if the list index is out of range
            if i >= len(list(pP1.keys())):
                break
            key = list(pP1.keys())[i]
            for row in data:
                if key in row.findAll('td')[0].b.text:
                    # If its a number, convert it to int
                    if key == "Key" or key == "Stress Level" or key == "Health" or key == "Movement Range" or key == "Attack Range" or key == "Attack Damage" or key == "Fire Damage" or key == "Electric Damage" or key == "Poison Damage":
                        pP1[key] = int(row.findAll('td')[1].text.replace(
                            "\n", "").split(" ")[0])
                    else:
                        # remove \n and spaces
                        pP1[key] = row.findAll('td')[1].text.replace(
                            "\n", "")
        if pP1["Race"].lower() == "monster":
            colorhu = 0xf57242
        elif pP1["Race"].lower() == "mechanical":
            colorhu = 0x42a1f5
        elif pP1["Race"].lower() == "dimensional":
            colorhu = 0xa533c4
        elif pP1["Race"].lower() == "undead":
            colorhu = 0x6f9e3c
        else:
            colorhu = 0xf57242

        embed = discord.Embed(
            title="<:Icon_KeyCost:967647459968950323>  "+str(pP1["Key"])+" - "+name, description="\"" + descriptions + "\"", color=colorhu)
        embed.set_thumbnail(url=url)
        embed.add_field(name="Race", value=pP1["Race"], inline=True)
        embed.add_field(
            name="<:Lippy:967789127212867604> Rarity", value=pP1["Rarity"], inline=True)
        embed.add_field(name="<:icon_health:967647464226185296> Health", value=int(
            pP1["Health"]), inline=True)
        embed.add_field(name=emojiFinder(pP1["Movement Type"], "movement")+" Movement Range", value=int(
            pP1["Movement Range"]), inline=True)
        embed.add_field(
            name=emojiFinder(pP1["Movement Type"], "movement")+" Movement Type", value=pP1["Movement Type"], inline=True)
        embed.add_field(name=emojiFinder(pP1["Attack Type"], "attack")+" Attack Range", value=int(
            pP1["Attack Range"]), inline=True) if pP1["Attack Range"] != 0 else None
        embed.add_field(name=emojiFinder(pP1["Attack Type"], "attack")+" Attack Type",
                        value=pP1["Attack Type"], inline=True) if pP1["Attack Type"] != "" else None
        embed.add_field(name="<:icon_damage:967647459587285052> Attack Damage", value=int(
            pP1["Attack Damage"]), inline=True) if pP1["Attack Damage"] != 0 else None
        embed.add_field(name=emojiFinder(pP1["Effect Type"], "effect")+" Effect Range",
                        value=pP1["Effect Range"], inline=True) if pP1["Effect Range"] != "" else None
        embed.add_field(name="<:icon_fire:967647463634792519> Fire Damage", value=int(
            pP1["Fire Damage"]), inline=True) if pP1["Fire Damage"] != 0 else None
        embed.add_field(name="<:icon_electrical:967647459562102834> Electric Damage", value=int(
            pP1["Electric Damage"]), inline=True) if pP1["Electric Damage"] != 0 else None
        embed.add_field(name="<:icon_poison:967647464570109952> Poison Damage", value=int(
            pP1["Poison Damage"]), inline=True) if pP1["Poison Damage"] != 0 else None
    elif page == 2:
        pP2 = phobieP2.copy()
        # test
        for i in range(0, 13):
            if i >= len(list(pP2.keys())):
                break
            key = list(pP2.keys())[i]
            for row in data:
                if key in row.findAll('td')[0].b.text:
                    # If its a number, convert it to int
                    if key == "Attack Damage" or key == "Effect Duration" or key == "Health" or key == "Additional Movement" or key == "Disease Damage":
                        pP2[key] = int(row.findAll('td')[1].text.replace(
                            "\n", "").split(" ")[0])
                    else:
                        # remove \n and spaces
                        pP2[key] = row.findAll('td')[1].text.replace(
                            "\n", "")
        embed = discord.Embed(
            title=descriptions, description=pP2["Description"], color=0xf57242)
        embed.set_thumbnail(url=url)
        embed.add_field(
            name="<:icon_leech:967647464737890346> HP Lifesteal", value=pP2["HP Lifesteal"], inline=True) if pP2["HP Lifesteal"] != "" else None
        embed.add_field(
            name="Resurrect HP", value=pP2["Health"], inline=True) if pP2["Health"] != 0 else None
        embed.add_field(name="<:clock:967647458018590781> Duration",
                        value=pP2["Effect Duration"], inline=True) if pP2["Effect Duration"] != 0 else None
        embed.add_field(name="<:icon_damage:967647459587285052> Effect Range",
                        value=pP2["Effect Range"], inline=True) if pP2["Effect Range"] != "" else None
        embed.add_field(name="<:icon_health:967647464226185296> HP Heal",
                        value=pP2["HP Heal"], inline=True) if pP2["HP Heal"] != "" else None
        embed.add_field(name="<:icon_damage:967647459587285052> Attack Damage",
                        value=pP2["Attack Damage"], inline=True) if pP2["Attack Damage"] != 0 else None
        embed.add_field(name="<:icon_damage:967647459587285052> Damage Buff",
                        value=pP2["Damage Buff"], inline=True) if pP2["Damage Buff"] != "" else None
        embed.add_field(name="<:icon_damage:967647459587285052> Reflect",
                        value=pP2["Attack Reflect"], inline=True) if pP2["Attack Reflect"] != "" else None
        embed.add_field(name="<:icon_electrical:967647459562102834> Electric Reflect",
                        value=pP2["Electric Reflect"], inline=True) if pP2["Electric Reflect"] != "" else None
        embed.add_field(name="<:Passive_Disease:967647465014706176> Disease Damage",
                        value=pP2["Disease Damage"], inline=True) if pP2["Disease Damage"] != "" else None
    elif page == 3:
        pP3 = phobieP3.copy()
        # test
        for i in range(0, 20):
            if i >= len(list(pP3.keys())):
                break
            key = list(pP3.keys())[i]
            for row in data:
                if key in row.findAll('td')[0].b.text:
                    # If its a number, convert it to int
                    if key == "Attack Damage" or key == "Additional Movement" or key == "Obstacle HP" or key == "Trap Damage" or key == "Electric Damage" or key == "Effect Duration" or key == "Cooldown" or key == "Unlocking" or key == "Movement Range":
                        pP3[key] = int(row.findAll('td')[1].text.replace(
                            "\n", "").split(" ")[0])
                    else:
                        # remove \n and spaces
                        pP3[key] = row.findAll('td')[1].text.replace(
                            "\n", "")
            embed = discord.Embed(
                title=descriptions, description=pP3["Description"], color=0xa533c4)
            embed.set_thumbnail(url=url)
            embed.add_field(name="<:icon_lock:967647459943788546> Unlocking",
                            value=pP3["Unlocking"], inline=True) if pP3["Unlocking"] != 0 else None
            embed.add_field(name="<:clock:967647458018590781> Cooldown",
                            value=pP3["Cooldown"], inline=True) if pP3["Cooldown"] != 0 else None
            embed.add_field(name="<:icon_leech:967647464737890346> Lifesteal",
                            value=pP3["Lifesteal"], inline=True) if pP3["Lifesteal"] != "" else None
            embed.add_field(name="<:clock:967647458018590781> Effect Duration",
                            value=pP3["Effect Duration"], inline=True) if pP3["Effect Duration"] != 0 else None
            embed.add_field(name=emojiFinder(pP3["Effect Range"], "effect")+" Effect Range",
                            value=pP3["Effect Range"], inline=True) if pP3["Effect Range"] != "" else None
            embed.add_field(name=emojiFinder(pP3["Attack Type"], "attack")+" Attack Type",
                            value=pP3["Attack Type"], inline=True) if pP3["Attack Type"] != "" else None
            embed.add_field(
                name="Movement Boost", value=pP3["Additional Movement"], inline=True) if pP3["Additional Movement"] != 0 else None
            embed.add_field(
                name="Obstacle HP", value=pP3["Obstacle HP"], inline=True) if pP3["Obstacle HP"] != 0 else None
            embed.add_field(
                name="HP Heal", value=pP3["HP Heal"], inline=True) if pP3["HP Heal"] != "" else None
            embed.add_field(name="<:icon_damage:967647459587285052> Attack Damage",
                            value=pP3["Attack Damage"], inline=True) if pP3["Attack Damage"] != 0 else None
            embed.add_field(name="<:icon_damage:967647459587285052> Damage Buff",
                            value=pP3["Damage Buff"], inline=True) if pP3["Damage Buff"] != "" else None
            embed.add_field(
                name="Damage Debuff", value=pP3["Damage Debuff"], inline=True) if pP3["Damage Debuff"] != "" else None
            embed.add_field(
                name="Trap Damage", value=pP3["Trap Damage"], inline=True) if pP3["Trap Damage"] != 0 else None
            embed.add_field(name="<:icon_movement_bypass:967647460631646289> Movement Range",
                            value=pP3["Movement Range"], inline=True) if pP3["Movement Range"] != 0 else None
            embed.add_field(name="<:icon_electrical:967647459562102834> Electric Damage",
                            value=pP3["Electric Damage"], inline=True) if pP3["Electric Damage"] != 0 else None
            embed.add_field(name="<:icon_fire:967647463634792519> Fire Damage",
                            value=pP3["Fire Damage"], inline=True) if pP3["Fire Damage"] != "" else None
            embed.add_field(name="<:icon_poison:967647464570109952> Poison Damage",
                            value=pP3["Poison Damage"], inline=True) if pP3["Poison Damage"] != "" else None
            embed.add_field(name="<:icon_disease:967647462883999757> Disease Damage",
                            value=pP3["Disease Damage"], inline=True) if pP3["Disease Damage"] != "" else None

    return embed


def setup(bot):
    bot.add_cog(wiki(bot))
