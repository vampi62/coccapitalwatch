@echo off

REM Remplacez les valeurs ci-dessous par celles de votre service
set "serviceName=coccapitalwatch"
set python_executable=python.exe
set python_script="%~dp0..\maindiscord.py"

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

sc create "%serviceName%" binPath= "%python_executable% %python_script%" start= auto

echo Service cree avec succes.