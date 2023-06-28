# coccapitalwatch

vous en avez marre de cette situation ou 3 gus de votre clan rust le hall de la capitale alors votre capitale est prema et se fait démonter chaque week-end

surveillez les donnations de gemmes dans la capitale de clan,
les changement sont enregistrer en base, il ne vous restera plus qu'a noté le nbr de gemme du hall, et si il change vous n'aurai plus qu'a rechercher dans la db pour trouver une correspondance


python 
```sh
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
```
```sh

[server]
# Protocol (http, https, h2, socket)
protocol = http

# The ip address to bind to, empty will bind to all interfaces
;http_addr =

# The http port  to use
http_port = 3000

# The public facing domain name used to access grafana from a browser
domain = site.ddns.net

# Redirect to correct domain if host header does not match domain
# Prevents DNS rebinding attacks
enforce_domain = false

# The full public facing url you use in browser, used for redirects and emails
# If you use reverse proxy and sub path specify full url (with sub path)
root_url = %(protocol)s://%(domain)s:%(http_port)s/
```
crontab
```sh
*/5 * * * * su pi -c "python /home/pi/coccapitalwatch/main.py"
```