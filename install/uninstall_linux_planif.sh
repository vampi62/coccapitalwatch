#!/bin/sh

# Supprimez la tâche Cron pour exécuter le script Python toutes les 5 minutes
repertoire_script=$(dirname "$(readlink -f "$0")")
chemin_python="$repertoire_script/../main.py"

# Créez une expression de recherche pour la tâche Cron à supprimer
recherche="*/5 * * * * python $chemin_python"

# Obtenez les tâches Cron actuelles
crontab -l > mycron

# Utilisez "grep -v" pour filtrer les lignes ne correspondant pas à l'expression de recherche
nouveau_cron=$(grep -v "$recherche" mycron)

# Installez la nouvelle configuration Cron sans la tâche spécifiée
echo "$nouveau_cron" | crontab -

# Supprimez le fichier temporaire
rm mycron

echo "La tâche Cron pour exécuter le script Python toutes les 5 minutes a été retirée."