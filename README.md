# coccapitalwatch

Vous en avez marre de cette situation ou 3 gus de votre clan rush le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

Surveillez les donations de gemmes dans la capitale de clan,
Les changements sont enregistrés en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et s’il change vous n'aurai plus qu'à rechercher dans la db pour trouver une correspondance

prérequis
- un pc ou de préférence un serveur (qui pourra fonctionner 24h/24)
- une cle api clash of clan (gratuits) https://developer.clashofclans.com/#/
- l'id du clan à surveillez

# menu

* [installation sur windows](#windows)
* [installation sur linux](#linux)

# windows

1) suivez les procedures d'installation des logiciels ci-dessous
selectionner les installer pas d'embedded

- telecharger le repo git https://github.com/vampi62/coccapitalwatch.git

- https://www.python.org/downloads/windows/
(lancer le programme et avant de cliquer sur install cocher les cases "use admin" et "add to PATH")

- https://dev.mysql.com/downloads/installer/
(mysql server only --> next jusqu'a install (changer le root password))

- https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/

2) ouvrez un cmd
installer les modules requis par python
```sh
pip install requests
pip install mysql-connector-python
```

dans la recherche windows ouvrer "mysqlcommande line client"
après avoir entrer le mot de passe root :
(changer "password")
```sh
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
FLUSH PRIVILEGES;
exit
```

- completer le fichier config.json

lancer l'installation de la base (changer le répertoire si besoin)
```sh
cd C:/Téléchargements/coccapitalwatch/
python C:/Téléchargements/coccapitalwatch/install.py
```

- creer une tache planifier

allez dans le planificateur de tache
creer une nouvelle tache avec une execution régulière
![declencheur](https://github.com/vampi62/coccapitalwatch/assets/104321401/bab9dd4c-f75e-41b3-aa35-880a9911fd0a)

ajouter l'action vers le script main ! executer dans le dossier du fichier main
![action](https://github.com/vampi62/coccapitalwatch/assets/104321401/b76b3a3d-ed74-4ee4-bbdf-bbbbd563b330)


# linux
```sh
sudo git clone https://github.com/vampi62/coccapitalwatch.git
cd coccapitalwatch
sudo apt install python
pip install requests
pip install mysql-connector-python
```
- une base de donnée
```sh 
sudo apt install mariadb-server
```
- un grafana pour visualiser les données
```sh
https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/
```

configurer la base de données
```sh
mysql -h localhost -u root -p
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('NouveauMotDePasse');
FLUSH PRIVILEGES;
exit
```

- completer le fichier config.json

lancer l'installation de la base (changer le répertoire si besoin)
```sh
cd ~/coccapitalwatch/
python ~/coccapitalwatch/install.py
```

- installer la tache planifier
crontab (remplacer "pi" par le nom de l'utilisateur qui stock le projet) (linux uniquement)
```sh
sudo crontab -e

*/5 * * * * su pi -c "python /home/pi/coccapitalwatch/main.py"
```
- executer : "su pi -c "python /home/pi/coccapitalwatch/main.py"
(verification du fonctionnement du script comme vue au-dessus remplacer pi)


# grafana

connecter vous a grafana :
naviagateur entrer localhost:3000

si le service fonctionne un login vous sera demander (admin:admin)


en bas a gauche aller dans administration > source de données

creer une source MYSQL et rempliser les informations de connexion
![sql](https://github.com/vampi62/coccapitalwatch/assets/104321401/d6cfc9a9-df56-428f-9e00-a20069dbbe42)

valider sur "save & test"

dans dashboard cliquer sur "new" > import

importer le dashboard coccapitalwatch-xxxx.json
changer le temps affichage sur UTC
![utc](https://github.com/vampi62/coccapitalwatch/assets/104321401/20367ef6-ecbb-4f06-824e-f5d276e442c7)



(la partie ci-dessous nécessite un suivie manuelle régulier, si vous voulez juste suivre les dépôts comme ce que faisait certain bot discord vous pouvez ignorer la suite)

- executer inserthall.py pour ajouter une messure de l'etat du hall --> dans le jeu recuperer le nombre de gemmes investie dans le hall entrer cette valeur dans la zone de saisie
```sh
python /home/pi/coccapitalwatch/insertall.py
```
cette dernière commande est à exécuter régulièrement pour bien suivre tout changement dans le hall.

le fichier "correspondance.py" permet de remonter comparer la difference entre 2 relever du hall pour trouver les depots responsable de ce changement.
exemple dans les image ci-joint.
![2hall](https://github.com/vampi62/coccapitalwatch/assets/104321401/184a5306-998f-4e2c-90ec-5b0c638399af)
![correspondance](https://github.com/vampi62/coccapitalwatch/assets/104321401/1936c7bb-bc0b-45b4-ad74-8fe62286b9af)

