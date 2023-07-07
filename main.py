import mysql.connector
import json
import os
import requests
import time
chemin = os.getcwd()
date = time.strftime('%Y-%m-%d %H:%M:%S')
date = str(date)
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
db_cursor.execute("SELECT * FROM joueurs")
dbplayer = db_cursor.fetchall()
for player in dbplayer:
    # supprimer les joueurs qui ne sont plus dans le clan
    found = False
    for member in clan_info["memberList"]:
        if member["tag"] == player[2]:
            found = True
            break
    if found == False:
        print("DELETE")
        db_cursor.execute("DELETE FROM joueurs WHERE tag_joueur = '" + str(player[2]) + "'")
db_connection.commit()

for member in clan_info["memberList"]:
    member_info = get_member_info(member["tag"], data['api_key'])
    #verifier si le joueur existe déjà dans la base de données
    #si oui, mettre à jour les informations
    #si non, l'ajouter
    db_cursor.execute("SELECT * FROM joueurs WHERE tag_joueur = '" + member["tag"] + "'")
    dbplayer = db_cursor.fetchall()
    if dbplayer:
        print(dbplayer[0])
        if int(member_info["clanCapitalContributions"]) != int(dbplayer[0][3]):
            update_query = "UPDATE joueurs SET contributions_joueur = %s, date_dernier_depot_joueur = %s WHERE tag_joueur = %s"
            values = (member_info["clanCapitalContributions"], date, member["tag"])
            db_cursor.execute(update_query, values)
            # ajoute une entrer dans la table depot
            print('UPDATE')
            print(str(int(member_info["clanCapitalContributions"])-int(dbplayer[0][3])))
            insert_query = "INSERT INTO depot (id_joueur, montant, date_depot) VALUES (%s, %s, %s)"
            values = (dbplayer[0][0], int(member_info["clanCapitalContributions"])-int(dbplayer[0][3]), date)
            db_cursor.execute(insert_query, values)
    else:
        insert_query = "INSERT INTO joueurs (pseudo_joueur, tag_joueur, contributions_joueur, date_dernier_depot_joueur) VALUES (%s, %s, %s, %s)"
        values = (member["name"], member["tag"], member_info["clanCapitalContributions"], date)
        print("ADD")
        print(values)
        db_cursor.execute(insert_query, values)
    

db_connection.commit()
db_connection.close()