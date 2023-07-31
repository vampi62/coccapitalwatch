import mysql.connector
import json
import os
import requests
with open(os.path.join(os.path.dirname(__file__), "../config.json"), encoding='utf-8') as fs:
      try:
        data = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur config.json not found")
        exit()

with open(os.path.join(os.path.dirname(__file__), "../lang/" + data['lang'] + ".json"), encoding='utf-8') as fs:
      try:
        lang = json.load(fs) # lecture json
        fs.close()
      except:
        fs.close()
        print("Erreur lang/" + data['lang'] + ".json not found")
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
        print(lang["install_erreur_api"])
        input(lang["input_exit"])
        exit()
except:
    print(lang["install_erreur_api"])
    input(lang["input_exit"])
    exit()

# test la connexion a la base mysql
try:
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()
    db_cursor.execute(open("coc.sql", "r").read())
    db_connection.close()
except:
    print(lang["error_db"])
    input(lang["input_exit"])
    exit()


print(lang["install_ok"])
input(lang["input_exit"])
exit()