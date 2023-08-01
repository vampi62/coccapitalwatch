#!/bin/bash

# Chemin complet vers le fichier Python # repertoire du fichier bash
repertoire_script=$(dirname "$(readlink -f "$0")")
chemin_python="$repertoire_script/../maindiscord.py"

# Créer le fichier de service
service_file="/etc/systemd/system/coccapitalwatch.service"
echo "[Unit]
Description=Mon service Python

[Service]
Type=simple
ExecStart=$chemin_python
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee $service_file

# Charger le service
sudo systemctl daemon-reload

# Activer le service pour qu'il démarre au démarrage du système
sudo systemctl enable coccapitalwatch

# Démarrer le service
sudo systemctl start coccapitalwatch

# Vérifier le statut du service
sudo systemctl status coccapitalwatch
