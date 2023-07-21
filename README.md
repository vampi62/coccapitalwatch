# coccapitalwatch

Vous en avez marre de cette situation ou 3 gus de votre clan rust le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

Surveillez les donations de gemmes dans la capitale de clan,
Les changements sont enregistrés en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et s’il change vous n'aurai plus qu'à rechercher dans la db pour trouver une correspondance

prérequis
- un pc ou de préférence un serveur (qui pourra fonctionner 24h/24)
- une cle api clash of clan (gratuits) https://developer.clashofclans.com/#/
- l'id du clan à surveillez


installation sur un poste windows

1) suivez les procedures d'installation des logiciels ci-dessous
https://www.python.org/downloads/windows/
https://dev.mysql.com/downloads/installer/
https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/

2) ouvrez un cmd
module requis par python
```sh
pip install requests
pip install mysql-connector-python
```

installation sur un poste linux
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




configuration sur linux ou windows


1) configuration des services

- base de données
(si vous n'êtes pas très à l’aise avec les commande, vous pouvez install phpmyadmin pour administrer votre base)
```sh
mysql -h localhost -u root -p
CREATE DATABASE coc
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
FLUSH PRIVILEGES;
exit
```

- completer le fichier config.json

2) mise en route
- executer le fichier install.py

pour linux
```sh
cd ~/coccapitalwatch/
python ~/coccapitalwatch/install.py
```

pour windows
```sh
cd C:/Téléchargements/coccapitalwatch/
python C:/Téléchargements/coccapitalwatch/install.py
```


dans grafana importer le dashboard coccapitalwatch-xxxx.json
creer un utilisateur qui a des acces vue uniquement si vous compter laisser un acces publique

- installer la tache planifier
crontab (remplacer "pi" par le nom de l'utilisateur qui stock le projet) (linux uniquement)
```sh
sudo crontab -e

*/5 * * * * su pi -c "python /home/pi/coccapitalwatch/main.py"
```
- executer : "su pi -c "python /home/pi/coccapitalwatch/main.py"
(verification du fonctionnement du script comme vue au-dessus remplacer pi)

allez dans le planificateur de tache
creer une nouvelle tache avec une execution régulière
![declencheur](https://github.com/vampi62/coccapitalwatch/assets/104321401/bab9dd4c-f75e-41b3-aa35-880a9911fd0a)

ajouter l'action vers le script main ! executer dans le dossier du fichier main
![action](https://github.com/vampi62/coccapitalwatch/assets/104321401/b76b3a3d-ed74-4ee4-bbdf-bbbbd563b330)


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

