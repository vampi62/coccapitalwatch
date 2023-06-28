# coccapitalwatch

vous en avez marre de cette situation ou 3 gus de votre clan rust le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

surveillez les donnations de gemmes dans la capitale de clan,
les changement sont enregistrer en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et si il change vous n'aurai plus qu'a rechercher dans la db pour trouver une correspondance




python 
```sh
sudo git clone https://github.com/vampi62/coccapitalwatch.git
cd coccapitalwatch
sudo apt install python
pip install requests
pip install mysql-connector-python
```

base de donnée
```sh 
sudo apt install mariadb-server
```

grafana
```sh
https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/
```
```sh
nano /var/lib/grafana/grafana.ini

[server]
protocol = http
;http_addr =
http_port = 3000
domain = site.ddns.net
enforce_domain = false
root_url = %(protocol)s://%(domain)s:%(http_port)s/
```
completer le fichier config.json (copie le chemin complet dans la variable fichier_config de chaque fichier python du projet)
executer le fichier install.py
```sh
python /home/pi/coccapitalwatch/install.py
```

dans grafana importer le dashboard coccapitalwatch-xxxx.json
creer un utilisateur qui a des acces vu uniquement

installer la tache planifier
crontab
```sh
sudo crontab -e

*/5 * * * * su pi -c "python /home/pi/coccapitalwatch/main.py"
```

executer inserthall.py pour ajouter une messure de l'etat du hall --> dans le jeu recuperer le nombre de gemmes investie dans le hall entrer cette valeur dans la zone de saisie
```sh
python /home/pi/coccapitalwatch/insertall.py
```

