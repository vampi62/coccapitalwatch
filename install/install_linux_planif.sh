#!/bin/sh
sudo pip install discord
sudo pip install mysql-connector-python
sudo pip install requests

# Obtenez les tâches Cron actuelles
crontab -l > mycron

# Ajoutez la nouvelle tâche pour exécuter le script Python toutes les 5 minutes
repertoire_script=$(dirname "$(readlink -f "$0")")
chemin_python="$repertoire_script/../main.py"

echo "*/5 * * * * python $chemin_python" >> mycron

# Installez la nouvelle configuration Cron
crontab mycron

# Supprimez le fichier temporaire
rm mycron

echo "La tâche Cron pour exécuter le script Python toutes les 5 minutes a été ajoutée."