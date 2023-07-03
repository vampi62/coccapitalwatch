import mysql.connector
import time
import json
date = time.strftime('%Y-%m-%d %H:%M:%S')
date = str(date)
target_sum = 0
numbers_list = []
fichier_config = "/home/pi/coccapitalwatch/config.json"
with open(fichier_config, encoding='utf-8') as fs:
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

db_cursor.execute("SELECT somme_hall, date_hall FROM coc.halls ORDER BY date_hall DESC LIMIT 2")
dbhall = db_cursor.fetchall()
target_sum = dbhall[0][0] - dbhall[1][0]
print("somme déposée : " + str(target_sum))
print("date de recherche : " + str(dbhall[1][1]))
db_cursor.execute("SELECT id_depot, montant FROM coc.depot WHERE date_depot > '" + str(dbhall[1][1]) + "'")
dbdepot = db_cursor.fetchall()
for depot in dbdepot:
    numbers_list.append(depot[1])
    print("somme déposer dans l'interval : " + str(depot[1]))



def find_combination(numbers, target_sum):
    # Trie la liste dans l'ordre croissant
    numbers.sort()
    # Initialise une liste vide pour stocker les éléments nécessaires
    combination = []
    # Utilise l'algorithme de la somme partielle
    def partial_sum(current_sum, remaining_numbers):
        if current_sum == target_sum:
            # Si la somme actuelle est égale à la somme cible, retourne la combinaison trouvée
            return combination
        elif current_sum > target_sum or len(remaining_numbers) == 0:
            # Si la somme actuelle dépasse la somme cible ou s'il ne reste plus d'éléments, retourne None
            return None
        else:
            # Parcourt les éléments restants
            for i, num in enumerate(remaining_numbers):
                # Ajoute l'élément à la combinaison actuelle
                combination.append(num)
                # Appelle récursivement la fonction avec la nouvelle somme et les éléments restants
                result = partial_sum(current_sum + num, remaining_numbers[i+1:])
                if result is not None:
                    # Si une combinaison valide a été trouvée, retourne-la
                    return result
                # Sinon, supprime l'élément ajouté de la combinaison
                combination.pop()

    # Appelle la fonction de calcul de la somme partielle avec la somme actuelle à 0 et tous les éléments de la liste
    return partial_sum(0, numbers)


result = find_combination(numbers_list, target_sum)

if result is None:
    print("Aucune combinaison trouvée pour atteindre la somme cible.")
else:
    print("Combinaison trouvée :", result)
print("atention : les petites sommes rondes peuvent correspondre exemple un 450 et un 550 peuvent être sortie par le programme alors qu'il pourrait s'agir d'un 1000")
input("Appuyez sur une touche pour quitter...")