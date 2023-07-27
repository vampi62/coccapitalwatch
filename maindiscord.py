import mysql.connector
import json
import os
import requests
import time
import asyncio
import discord
chemin = os.getcwd()
date = str(time.strftime('%Y-%m-%d %H:%M:%S'))

with open(chemin + "/config.json", encoding='utf-8') as fs:
      try:
        data = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur lors de la lecture du fichier config.json")
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
    global db_connection
    global db_cursor
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(int(data['discord_channel']))
    if channel:
        await channel.send("Bot connecté !")
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
    global db_connection
    global db_cursor
    try:
        db_connection.is_connected()
    except:
        connectsql()
    if not nbr_jeton.isdigit():
        print("Erreur, le nombre de jeton doit être un nombre")
        return ["Erreur, le nombre de jeton doit être un nombre"]
    try:
        insert_query = "INSERT INTO halls (somme_hall, date_hall) VALUES (%s, %s)"
        values = (nbr_jeton,date)
        db_cursor.execute(insert_query, values)
        db_connection.commit()
    except:
        print("Erreur lors de la connexion à la base de données")
        return ["Erreur lors de la connexion à la base de données"]
    print("donnée mise à jour avec succès !")
    return ["donnée mise à jour avec succès !"]

def correspondance():
    global db_connection
    global db_cursor
    try:
        db_connection.is_connected()
    except:
        connectsql()
    returnmessage = []
    target_sum = 0
    numbers_list = []
    db_cursor.execute("SELECT somme_hall, date_hall FROM coc.halls ORDER BY date_hall DESC LIMIT 2")
    dbhall = db_cursor.fetchall()
    target_sum = dbhall[0][0] - dbhall[1][0]
    print("somme déposée : " + str(target_sum))
    print("date de recherche : " + str(dbhall[1][1]))
    returnmessage.append("somme déposée : " + str(target_sum))
    returnmessage.append("date de recherche : " + str(dbhall[1][1]))
    db_cursor.execute("SELECT id_depot, montant FROM coc.depot WHERE date_depot > '" + str(dbhall[1][1]) + "'")
    dbdepot = db_cursor.fetchall()
    for depot in dbdepot:
        numbers_list.append(depot[1])
        print("somme déposer dans l'interval : " + str(depot[1]))
        returnmessage.append("somme déposer dans l'interval : " + str(depot[1]))
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
        print("Aucune combinaison trouvée pour atteindre la somme cible.")
        returnmessage.append("Aucune combinaison trouvée pour atteindre la somme cible.")
    else:
        print("Combinaison trouvée : " + str(result))
        print("attention : les petites sommes rondes peuvent correspondre, par exemple un 450 et un 550 peuvent être sorti par le programme alors qu'il pourrait s'agir d'un 1000.")
        returnmessage.append("Combinaison trouvée : " + str(result))
        returnmessage.append("attention : les petites sommes rondes peuvent correspondre, par exemple un 450 et un 550 peuvent être sorti par le programme alors qu'il pourrait s'agir d'un 1000.")
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
        await your_function_to_run_periodically()
        await asyncio.sleep(300)

async def your_function_to_run_periodically():
    global db_connection
    global db_cursor
    try:
        db_connection.is_connected()
    except:
        connectsql()
    returnmessage = []
    clan_info = get_clan_info(data['clan_tag'], data['api_key'])
    db_cursor.execute("SELECT * FROM joueurs")
    dbplayer = db_cursor.fetchall()
    # supprimer les joueurs qui ne sont plus dans le clan
    for player in dbplayer:
        found = False
        for member in clan_info["memberList"]:
            if member["tag"] == player[2]:
                found = True
                break
        if found == False:
            print("DELETE")
            db_cursor.execute("DELETE FROM joueurs WHERE tag_joueur = '" + str(player[2]) + "'")
    db_connection.commit()
    # mettre à jour les informations des joueurs
    for member in clan_info["memberList"]:
        member_status = []
        member_info = get_member_info(member["tag"], data['api_key'])
        #verifier si le joueur existe déjà dans la base de données
        #si oui, mettre à jour les informations
        #si non, l'ajouter
        db_cursor.execute("SELECT * FROM joueurs WHERE tag_joueur = '" + member["tag"] + "'")
        dbplayer = db_cursor.fetchall()
        if dbplayer:
            print(dbplayer[0])
            member_status.append(member["name"])
            if int(member_info["clanCapitalContributions"]) != int(dbplayer[0][3]):
                update_query = "UPDATE joueurs SET contributions_joueur = %s, date_dernier_depot_joueur = %s WHERE tag_joueur = %s"
                values = (member_info["clanCapitalContributions"], date, member["tag"])
                db_cursor.execute(update_query, values)
                # ajoute une entrer dans la table depot
                print('UPDATE')
                print(str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])))
                member_status.append("UPDATE")
                member_status.append(str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])))
                insert_query = "INSERT INTO depot (id_joueur, montant, date_depot) VALUES (%s, %s, %s)"
                values = (dbplayer[0][0], int(member_info["clanCapitalContributions"])-int(dbplayer[0][3]), date)
                db_cursor.execute(insert_query, values)
                returnmessage.append(str(member_status))
        else:
            insert_query = "INSERT INTO joueurs (pseudo_joueur, tag_joueur, contributions_joueur) VALUES (%s, %s, %s)"
            values = (member["name"], member["tag"], member_info["clanCapitalContributions"])
            print("ADD")
            print(values)
            member_status.append(member["name"])
            member_status.append("ADD")
            member_status.append("")
            db_cursor.execute(insert_query, values)
            returnmessage.append(str(member_status))
    db_connection.commit()
    channel = bot.get_channel(int(data['discord_channel']))
    if channel:
        for msg in returnmessage:
            print(msg)
            await channel.send(msg)
    else:
        print("Erreur, le channel discord n'est pas valide")

@bot.event
async def on_disconnect():
    db_connection.close()
    print('Connexion à la base de données fermée.')

bot.run(data['discord_token'])