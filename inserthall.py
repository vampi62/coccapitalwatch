import json
import mysql.connector
import time
date = time.strftime('%Y-%m-%d %H:%M:%S')
date = str(date)

with open("config.json", encoding='utf-8') as fs:
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
nbr_jeton = input("indique le nombre de jetons dans le hall de clan : ")

if not nbr_jeton.isdigit():
    print("Erreur, le nombre de jeton doit être un nombre")
    input("Appuyez sur une touche pour quitter...")
    exit()

try:
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()
    
    insert_query = "INSERT INTO halls (somme_hall, date_hall) VALUES (%s, %s)"
    values = (nbr_jeton,date)
    db_cursor.execute(insert_query, values)
    db_connection.commit()
    db_connection.clase()
except:
    print("Erreur lors de la connexion à la base de données")
    input("Appuyez sur une touche pour quitter...")
    exit()

print("donnée mise à jour avec succès !")
input("Appuyez sur une touche pour quitter...")
exit()