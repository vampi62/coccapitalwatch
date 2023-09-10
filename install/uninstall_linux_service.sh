#!/bin/sh
sudo systemctl stop coccapitalwatch
sudo systemctl disable coccapitalwatch
sudo rm /etc/systemd/system/coccapitalwatch.service
sudo systemctl daemon-reload

recherche="12 3 * * * sudo service coccapitalwatch restart"
crontab -l > mycron
nouveau_cron=$(grep -v "$recherche" mycron)
echo "$nouveau_cron" | crontab -
rm mycron