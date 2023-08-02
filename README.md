# coccapitalwatch

Vous en avez marre de cette situation ou 3 gus de votre clan rush le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

Surveillez les donations de gemmes dans la capitale de clan,
Les changements sont enregistrés en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et s’il change vous n'aurai plus qu'à rechercher dans la db pour trouver une correspondance


# coccapitalwatch

## menu
==================
* [coccapitalwatch](#coccapitalwatch)
    * [menu](#menu)
    * [pre-requis](#pre-requis)
    * [installation windows](#installation-sur-windows)
        * [telechargement](#telechargement)
        * [module python](#module-python)
        * [configuration db sql](#configuration-db-sql)
        * [(optionnel) discord bot](#optionnel-discord-bot)
        * [config.json](#configuration-fichier-configjson)
        * [install table sql](#configuration-table-sql)
        * [service ou tache](#service-windows)
        * [grafana](#grafana)
    * [installation linux](#installation-sur-linux)
        * [telechargement](#telechargement-1)
        * [module python](#module-python-1)
        * [configuration db sql](#configuration-db-sql-1)
        * [(optionnel) discord bot](#optionnel-discord-bot-1)
        * [config.json](#configuration-fichier-configjson-1)
        * [install table sql](#configuration-table-sql-1)
        * [service ou tache](#service-linux)
        * [grafana](#grafana-1)
    * [suivie du hall](#suivie-du-hall)
    * [desinstallation](#desinstallation)

## pre-requis
- un pc ou de préférence un serveur (qui pourra fonctionner 24h/24)
- une cle api clash of clan (gratuits) https://developer.clashofclans.com/#/
- l'id du clan à surveillez

## installation-sur-windows

### telechargement
suivez les procedures d'installation des logiciels ci-dessous
selectionner les installer pas d'embedded

- telecharger le repo git https://github.com/vampi62/coccapitalwatch.git

- https://www.python.org/downloads/windows/
(lancer le programme et avant de cliquer sur install cocher les cases "use admin" et "add to PATH")

- https://dev.mysql.com/downloads/installer/
(mysql server only --> next jusqu'a install (changer le root password))

- https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/ (optionnel si vous utiliser le script avec discord)

### module-python
ouvrer un cmd
installer les modules requis par python
```sh
pip install requests
pip install mysql-connector-python
```

### configuration-db-sql
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
### optionnel-discord-bot
si vous voulez utiliser le bot discord
```sh
pip install discord
```

sur le site de discord https://discord.com/developers/applications
- créer une application
- créer un bot
- ajouter le droit "message content intent" dans le menu "bot"
- copier le token
- connecter le bot a votre serveur
- copier l'id du channel ou vous voulez que le bot poste


### configuration-fichier-configjson
completer le fichier config.json

- bdip : l'ip de votre base de donnée
- bdport : le port de votre base de donnée
- bduser : l'utilisateur de votre base de donnée
- bdpass : le mot de passe de votre base de donnée
- bdname : le nom de votre base de donnée
- api_key : votre cle api clash of clan
- clan_tag : l'id du clan a surveillez
- discord_token : le token du bot discord (si vous n'utilisez pas discord laisser vide)
- discord_channel : l'id du channel ou vous voulez que le bot poste (si vous n'utilisez pas discord laisser vide)
- lang : fr ou en

### configuration-table-sql
lancer l'installation de la base (changer le répertoire si besoin)
```sh
python C:/Téléchargements/coccapitalwatch/install/install_db.py
```

### service-windows

- installer le service ou la tache planifier en fonction de si vous utiliser discord ou non
service si vous utiliser avec discord
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_service.bat
```

tache planifier si vous n'utilisez pas discord
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_planif.bat
```

### grafana

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

## installation-sur-linux

### telechargement
https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/

```sh
sudo apt install python
sudo apt install mariadb-server
```

### module-python
```sh
pip install requests
pip install mysql-connector-python
```

### configuration-db-sql
```sh
sudo mysql -u root -p
```
```sh
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('NouveauMotDePasse');
FLUSH PRIVILEGES;
exit
```
### optionnel-discord-bot
si vous voulez utiliser le bot discord
```sh
pip install discord
```

sur le site de discord https://discord.com/developers/applications
- créer une application
- créer un bot
- ajouter le droit "message content intent" dans le menu "bot"
- copier le token
- connecter le bot a votre serveur
- copier l'id du channel ou vous voulez que le bot poste

### configuration-fichier-configjson
completer le fichier config.json

- bdip : l'ip de votre base de donnée
- bdport : le port de votre base de donnée
- bduser : l'utilisateur de votre base de donnée
- bdpass : le mot de passe de votre base de donnée
- bdname : le nom de votre base de donnée
- api_key : votre cle api clash of clan
- clan_tag : l'id du clan a surveillez
- discord_token : le token du bot discord (si vous n'utilisez pas discord laisser vide)
- discord_channel : l'id du channel ou vous voulez que le bot poste (si vous n'utilisez pas discord laisser vide)
- lang : fr ou en

### configuration-table-sql
lancer l'installation de la base (changer le répertoire si besoin)
```sh
python ~/coccapitalwatch/install/install_db.py
```

### service-linux
- installer le service ou la tache planifier en fonction de si vous utiliser discord ou non
service si vous utiliser avec discord
```sh
python ~/coccapitalwatch/install/install_linux_service.sh
```
tache planifier si vous n'utilisez pas discord
```sh
python ~/coccapitalwatch/install/install_linux_planif.sh
```

### grafana

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


## suivi-du-hall

si vous n'utilisez pas le service discord vous pouvez suivre l'etat du hall en inserant les valeurs dans la base de donnée, pour cela il faut :
- executer inserthall.py pour ajouter une messure de l'etat du hall --> dans le jeu recuperer le nombre de gemmes investie dans le hall entrer cette valeur dans la zone de saisie
apres avoir inserer cette valeur en base le script va comparer la difference entre cette valeur et la dernière enregistrer avant pour trouver les depots responsable de ce changement.
```sh
python insertall.py
```
exemple dans les image ci-joint.
![2hall](https://github.com/vampi62/coccapitalwatch/assets/104321401/184a5306-998f-4e2c-90ec-5b0c638399af)
![correspondance](https://github.com/vampi62/coccapitalwatch/assets/104321401/1936c7bb-bc0b-45b4-ad74-8fe62286b9af)

si vous utilisez le service discord entrer la valeur dans le channel discord ou le bot poste les messages :
/insert __valeur_du_hall__ -- pour inserer une valeur et avoir le detail des depots responsable de ce changement
/reset 0 -- pour remettre a 0 le compteur du hall

## desinstallation

### service-windows
executez le fichier uninstall_ correspondant a votre installation : 
__os_utiliser__ : windows ou linux
__service_ou_planif__ : service ou planif (service si discord est utiliser sinon planif)
/coccapitalwatch/install/uninstall_ __os_utiliser__ _ __service_ou_planif__