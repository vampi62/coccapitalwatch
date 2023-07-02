# coccapitalwatch

Vous en avez marre de cette situation ou 3 gus de votre clan rust le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

Surveillez les donations de gemmes dans la capitale de clan,
Les changements sont enregistrés en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et s’il change vous n'aurai plus qu'à rechercher dans la db pour trouver une correspondance

1) sur la machine, vm ou autre qui servira de serveur il vous faut :
- python (avec les module request et mysql-connect)
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

si vous voulez accéder a votre vue grafana depuis l'exterieur ou la partager, il vous faut dans la config de votre box :
- fixer l'ip de votre serveur
- ouvrir le port 3000 et le rediriger vers l'ip du serveur
- ajouter une connexion a un service de ddns (ex : no-ip)

2) configuration des service

- service grafana, copier le conytenue ci-dessous dans le fichier : /var/lib/grafana/grafana.ini
(remplacer "site.ddns.net" par le nom de domaine que vous avez creer)
```sh
[server]
protocol = http
;http_addr =
http_port = 3000
domain = site.ddns.net
enforce_domain = false
root_url = %(protocol)s://%(domain)s:%(http_port)s/
```

- base de donnée
(si vous n'êtes pas très à l’aise avec les commande, vous pouvez install phpmyadmin pour administrer votre base)
```sh
mysql -h localhost -u root -p
CREATE DATABASE coc
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
FLUSH PRIVILEGES;
exit
```

- completer le fichier config.json et copier son chemin complet dans les variables "fichier_config" de chaque fichier python du projet)

3) mise en route
- executer le fichier install.py
```sh
python ~/coccapitalwatch/install.py
```

dans grafana importer le dashboard coccapitalwatch-xxxx.json
creer un utilisateur qui a des acces vue uniquement si vous compter laisser un acces publique

- installer la tache planifier
crontab (remplacer "pi" par le nom de l'utilisateur qui stock le projet)
```sh
sudo crontab -e

*/5 * * * * su pi -c "python /home/pi/coccapitalwatch/main.py"
```
- executer : "su pi -c "python /home/pi/coccapitalwatch/main.py"
(verification du fonctionnement du script comme vue au-dessus remplacer pi)


- executer inserthall.py pour ajouter une messure de l'etat du hall --> dans le jeu recuperer le nombre de gemmes investie dans le hall entrer cette valeur dans la zone de saisie
```sh
python /home/pi/coccapitalwatch/insertall.py
```
cette dernière commande est à exécuter régulièrement pour bien suivre tout changement dans le hall.

