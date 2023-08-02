@echo off
set python_executable=python.exe
set python_script="%~dp0..\main.py"

REM Vérification de l'emplacement de l'interpréteur Python
where /q %python_executable%
if %errorlevel% neq 0 (
    echo Erreur : Python not found.
    pause
    exit /b
)

REM Vérification de l'existence du script Python
if not exist %python_script% (
    echo Erreur : Script main not found.
    pause
    exit /b
)

pip install discord
pip install mysql-connector-python
pip install requests

REM Suppression de la tâche planifiée si elle existe déjà
schtasks /Delete /TN "coccapitalwatch" /F

REM Création de la nouvelle tâche planifiée pour s'exécuter toutes les 5 minutes
schtasks /Create /TN "coccapitalwatch" /TR "%python_executable% %python_script%" /SC MINUTE /MO 5

echo Tache planifiee cree avec succes.
pause
