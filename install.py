import mysql.connector
import json
import os
import requests
chemin = os.getcwd()
with open(chemin + "/config.json", encoding='utf-8') as fs:
      try:
        data = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur lors de la lecture du fichier config.json")
        input("Appuyez sur une touche pour quitter...")
        exit()

db_config = {
    "user": data['bduser'],
    "port": data['bdport'],
    "password":  data['bdpass'],
    "host":  data['bdip'],
    "database":  data['bdname']
}

# test la connexion a l'api clash of clans
try:
    clan_tag = data['clan_tag'].replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{clan_tag}"
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {data['api_key']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Erreur lors de la connexion à l'api clash of clans")
        input("Appuyez sur une touche pour quitter...")
        exit()
except:
    print("Erreur lors de la connexion à l'api clash of clans")
    input("Appuyez sur une touche pour quitter...")
    exit()

# test la connexion a la base mysql
try:
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()
    db_cursor.execute(open("coc.sql", "r").read())
    db_connection.close()
except:
    print("Erreur lors de la connexion à la base de données")
    input("Appuyez sur une touche pour quitter...")
    exit()


print("Installation terminée avec succès !")
input("Appuyez sur une touche pour quitter...")
exit()