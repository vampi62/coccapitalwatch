#!/bin/sh
sudo systemctl stop coccapitalwatch
sudo systemctl disable coccapitalwatch
sudo rm /etc/systemd/system/coccapitalwatch.service
sudo systemctl daemon-reload