@echo off

REM Remplacez cette valeur par le nom du service que vous souhaitez supprimer
set "serviceName=coccapitalwatch"

REM Arrêtez d'abord le service avant de le supprimer (facultatif)
sc stop "%serviceName%"

REM Supprimez le service à l'aide de la commande "sc"
sc delete "%serviceName%"

echo Service supprimé avec succès.