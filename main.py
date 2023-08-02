import mysql.connector
import json
import os
import requests
import time
date_insert = str(time.strftime('%Y-%m-%d %H:%M:%S'))
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
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

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
        db_cursor.execute("UPDATE joueurs SET tag_joueur = NULL WHERE tag_joueur = '" + str(player[2]) + "'")
db_connection.commit()

for member in clan_info["memberList"]:
    member_info = get_member_info(member["tag"], data['api_key'])
    #verifier si le joueur existe déjà dans la base de données
    #si oui, mettre à jour les informations
    #si non, l'ajouter
    db_cursor.execute("SELECT * FROM joueurs WHERE tag_joueur = '" + member["tag"] + "'")
    dbplayer = db_cursor.fetchall()
    if dbplayer:
        if int(member_info["clanCapitalContributions"]) != int(dbplayer[0][3]):
            update_query = "UPDATE joueurs SET contributions_joueur = %s, date_dernier_depot_joueur = %s WHERE tag_joueur = %s"
            values = (member_info["clanCapitalContributions"], date_insert, member["tag"])
            db_cursor.execute(update_query, values)
            # ajoute une entrer dans la table depot
            print(member["name"] + lang["depot_player_1"] + str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])) + lang["depot_player_2"] + date_insert + ".")
            insert_query = "INSERT INTO depot (id_joueur, montant, date_depot) VALUES (%s, %s, %s)"
            values = (dbplayer[0][0], int(member_info["clanCapitalContributions"])-int(dbplayer[0][3]), date_insert)
            db_cursor.execute(insert_query, values)
    else:
        insert_query = "INSERT INTO joueurs (pseudo_joueur, tag_joueur, contributions_joueur) VALUES (%s, %s, %s)"
        values = (member["name"], member["tag"], member_info["clanCapitalContributions"])
        print(member["name"] + lang['new_player'] + date_insert + ".")
        db_cursor.execute(insert_query, values)
    

db_connection.commit()
db_connection.close()