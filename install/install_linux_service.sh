#!/bin/sh
sudo pip install discord
sudo pip install mysql-connector-python
sudo pip install requests

# Chemin complet vers le fichier Python # repertoire du fichier bash
repertoire_script=$(dirname "$(readlink -f "$0")")
chemin_python="$repertoire_script/../maindiscord.py"

# Créer le fichier de service
service_file="/etc/systemd/system/coccapitalwatch.service"
echo "[Unit]
Description=Mon service Python

[Service]
Type=simple
ExecStart=python $chemin_python
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee $service_file

# Charger le service
sudo systemctl daemon-reload

# Activer le service pour qu'il démarre au démarrage du système
sudo systemctl enable coccapitalwatch

# Démarrer le service
sudo systemctl start coccapitalwatch

# Ajouter une tâche cron pour redémarrer le service toutes les jours
crontab -l > mycron
echo "12 3 * * * sudo service coccapitalwatch restart" >> mycron
crontab mycron
rm mycron

# Vérifier le statut du service
sudo systemctl status coccapitalwatch
