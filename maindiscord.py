import mysql.connector
import json
import os
import requests
import time
import asyncio
import discord
with open(os.path.join(os.path.dirname(__file__), "config.json"), encoding='utf-8') as fs:
      try:
        data = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur config.json not found")
        exit()

with open(os.path.join(os.path.dirname(__file__), "lang/" + data['lang'] + ".json"), encoding='utf-8') as fs:
      try:
        lang = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur lang/" + data['lang'] + ".json not found")
        exit()

# Informations de connexion à la base de données MariaDB
db_config = {
    "user": data['bduser'],
    "port": data['bdport'],
    "password":  data['bdpass'],
    "host":  data['bdip'],
    "database":  data['bdname']
}
def connectsql():
    db_connection = mysql.connector.connect(**db_config)
    return db_connection

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    bot.loop.create_task(insert_periodically())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if int(message.channel.id) == int(data['discord_channel']):
        if message.content.startswith('/insert'):
            returnmessage1 = inserthall(message.content.split('/insert ')[1])
            returnmessage2 = correspondance()
            returnmessage = returnmessage1 + returnmessage2
            await sendmessage(message,returnmessage)
        if message.content.startswith('/reset'):
            await message.channel.send(message.content)
            returnmessage = inserthall(message.content.split('/reset ')[1])
            await sendmessage(message,returnmessage)

async def sendmessage(message,returnmessage):
    for msg in returnmessage:
        await message.channel.send(msg)

def inserthall(nbr_jeton):
    db_connection = connectsql()
    db_cursor = db_connection.cursor()
    date_insert = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    if not nbr_jeton.isdigit():
        print(lang['error_number'])
        return [lang['error_number']]
    try:
        insert_query = "INSERT INTO halls (somme_hall, date_hall) VALUES (%s, %s)"
        values = (nbr_jeton,date_insert)
        db_cursor.execute(insert_query, values)
        db_connection.commit()
    except:
        print(lang['error_db'])
        return [lang['error_db']]
    print(lang['updatehall'])
    db_connection.close()
    return [lang['updatehall']]

def correspondance():
    db_connection = connectsql()
    db_cursor = db_connection.cursor()
    returnmessage = []
    target_sum = 0
    numbers_list = []
    db_cursor.execute("SELECT somme_hall, date_hall FROM coc.halls ORDER BY date_hall DESC LIMIT 2")
    dbhall = db_cursor.fetchall()
    target_sum = dbhall[0][0] - dbhall[1][0]
    print(lang["depot_hall"] + str(target_sum))
    print(lang["depot_date"] + str(dbhall[1][1]))
    returnmessage.append(lang["depot_hall"] + str(target_sum))
    returnmessage.append(lang["depot_date"] + str(dbhall[1][1]))
    db_cursor.execute("SELECT id_depot, montant FROM coc.depot WHERE date_depot > '" + str(dbhall[1][1]) + "'")
    dbdepot = db_cursor.fetchall()
    for depot in dbdepot:
        numbers_list.append(depot[1])
    print(lang["depot_interval"] + str(numbers_list))
    returnmessage.append(lang["depot_interval"] + str(numbers_list))
    def find_combination(numbers, target):
        numbers.sort()
        combination = []
        def partial_sum(current_sum, remaining_numbers):
            if current_sum == target:
                return combination
            elif current_sum > target or len(remaining_numbers) == 0:
                return None
            else:
                for i, num in enumerate(remaining_numbers):
                    combination.append(num)
                    result = partial_sum(current_sum + num, remaining_numbers[i+1:])
                    if result is not None:
                        return result
                    combination.pop()
        return partial_sum(0, numbers)
    result = find_combination(numbers_list, target_sum)
    if result is None:
        print(lang['error_combination'])
        returnmessage.append(lang['error_combination'])
    else:
        print(lang['combination_found'] + str(result))
        print(lang['attention'])
        returnmessage.append(lang['combination_found'] + str(result))
        returnmessage.append(lang['attention'])
    db_connection.close()
    return returnmessage

def get_clan_info(clan_tag, api_key):
    clan_tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{clan_tag}"
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data

def get_member_info(player_tag, api_key):
    player_tag = player_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/players/{player_tag}"
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data

async def insert_periodically():
    while True:
        await sync_clans()
        await asyncio.sleep(120)

async def sync_clans():
    db_connection = connectsql()
    db_cursor = db_connection.cursor()
    returnmessage = []
    date_insert = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    channel = bot.get_channel(int(data['discord_channel']))
    if not channel:
        print(lang['error_channel'])
    clan_info = get_clan_info(data['clan_tag'], data['api_key'])
    db_cursor.execute("SELECT id_joueur,pseudo_joueur,tag_joueur FROM joueurs WHERE tag_joueur IS NOT NULL")
    dbplayer = db_cursor.fetchall()
    # supprimer les joueurs qui ne sont plus dans le clan
    for player in dbplayer:
        found = False
        for member in clan_info["memberList"]:
            if member["tag"] == player[2]:
                found = True
                break
        if found == False:
            print(str(player[1]) + lang["left_clan"] + date_insert + ".")
            returnmessage.append(str(player[1]) + lang["left_clan"] + date_insert + ".")
            db_cursor.execute("UPDATE joueurs SET tag_joueur = NULL WHERE tag_joueur = '" + str(player[2]) + "'")
    db_connection.commit()
    # test - permet a discord de rester connecté
    await asyncio.sleep(1)
    # mettre à jour les informations des joueurs
    for member in clan_info["memberList"]:
        member_info = get_member_info(member["tag"], data['api_key'])
        #verifier si le joueur existe déjà dans la base de données
        #si oui, mettre à jour les informations
        #si non, l'ajouter
        # test - permet a discord de rester connecté
        await asyncio.sleep(0.2)
        db_cursor.execute("SELECT * FROM joueurs WHERE tag_joueur = '" + member["tag"] + "'")
        dbplayer = db_cursor.fetchall()
        if dbplayer:
            if int(member_info["clanCapitalContributions"]) != int(dbplayer[0][3]):
                update_query = "UPDATE joueurs SET contributions_joueur = %s, date_dernier_depot_joueur = %s WHERE tag_joueur = %s"
                values = (member_info["clanCapitalContributions"], date_insert, member["tag"])
                db_cursor.execute(update_query, values)
                insert_query = "INSERT INTO depot (id_joueur, montant, date_depot) VALUES (%s, %s, %s)"
                values = (dbplayer[0][0], int(member_info["clanCapitalContributions"])-int(dbplayer[0][3]), date_insert)
                db_cursor.execute(insert_query, values)
                print(member["name"] + lang["depot_player_1"] + str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])) + lang["depot_player_2"] + date_insert + ".")
                returnmessage.append(member["name"] + lang["depot_player_1"] + str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])) + lang["depot_player_2"] + date_insert + ".")
        else:
            insert_query = "INSERT INTO joueurs (pseudo_joueur, tag_joueur, contributions_joueur) VALUES (%s, %s, %s)"
            values = (member["name"], member["tag"], member_info["clanCapitalContributions"])
            db_cursor.execute(insert_query, values)
            print(member["name"] + lang['new_player'] + date_insert + ".")
            returnmessage.append(member["name"] + lang['new_player'] + date_insert + ".")
    db_connection.commit()
    # test - permet a discord de rester connecté
    await asyncio.sleep(1)
    if channel:
        for msg in returnmessage:
            await channel.send(msg)
    db_connection.close()

@bot.event
async def on_disconnect():
    print(lang['error_disconnect'])

bot.run(data['discord_token'])