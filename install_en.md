# coccapitalwatch
Tired of the situation where three players from your clan rush the Clan Hall in the capital, and as a result, your capital gets demolished every weekend?

Monitor gem donations in the clan capital. Changes are recorded in the database, and it is possible to connect a Discord bot that will post donations, arrivals, and departures in the clan.

## Menu
==================
* [coccapitalwatch](#coccapitalwatch)
    * [menu](#menu)
    * [pre-requis](#pre-requis)
    * [installation on Windows](#installation-sur-windows)
        * [download](#telechargement)
        * [Python module](#module-python)
        * [SQL database configuration](#configuration-db-sql)
        * [(optional) Discord bot](#optionnel-discord-bot)
        * [config.json](#configuration-fichier-configjson)
        * [install SQL table](#configuration-table-sql)
        * [service or task](#service-windows)
        * [Grafana](#grafana)
    * [installation on Linux](#installation-sur-linux)
        * [download](#telechargement-1)
        * [Python module](#module-python-1)
        * [SQL database configuration](#configuration-db-sql-1)
        * [(optional) Discord bot](#optionnel-discord-bot-1)
        * [config.json](#configuration-fichier-configjson-1)
        * [install SQL table](#configuration-table-sql-1)
        * [service or task](#service-linux)
        * [Grafana](#grafana-1)
    * [Clan Hall monitoring](#suivie-du-hall)
    * [uninstallation](#desinstallation)

## Prerequisites
- A PC or preferably a server (that can run 24/7).
- A Clash of Clans API key (free) from https://developer.clashofclans.com/#/.
- The clan ID you want to monitor.

## Installation on Windows

### Download
Follow the installation procedures for the software below. Choose to install them, not embedded.

- Download the Git repository: https://github.com/vampi62/coccapitalwatch.git

- Python: https://www.python.org/downloads/windows/ (Launch the program, check "Use admin" and "Add to PATH" before clicking on install)

- MySQL Server: https://dev.mysql.com/downloads/installer/ (Choose MySQL Server only, click Next until the installation is complete, and set the root password)

- Grafana (optional if using the script with Discord): https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/

### Python module
Open a command prompt and install the required Python modules:
```sh
pip install requests
pip install mysql-connector-python
```

### SQL database configuration
Open the Windows search and find "mysql command line client." After entering the root password (change "password"):
```sh
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
FLUSH PRIVILEGES;
exit
```

### Optional Discord bot
If you want to use the Discord bot:
```sh
pip install discord
```

On the Discord website https://discord.com/developers/applications:
- Create an application
- Create a bot
- Add the "message content intent" permission in the "Bot" menu
- Copy the token
- Connect the bot to your Discord server (the bot should have "read message," "send message," "read message history," and "send messages in threads" permissions)
- Copy the channel ID where you want the bot to post messages.

### Configuring the config.json file
Complete the config.json file:
- bdip: the IP address of your database
- bdport: the port of your database
- bduser: the database user
- bdpass: the database password
- bdname: the name of your database
- api_key: your Clash of Clans API key
- clan_tag: the ID of the clan to monitor
- discord_token: the Discord bot token (leave empty if not using Discord)
- discord_channel: the channel ID where you want the bot to post messages (leave empty if not using Discord)
- lang: fr or en

### Configuring the SQL table
Run the database installation script (change the directory if necessary):
```sh
python C:/Téléchargements/coccapitalwatch/install/install_db.py
```

### Service on Windows

- Install the service or scheduled task depending on whether you are using Discord or not:
Service if using Discord:
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_service.bat
```
Scheduled task if not using Discord:
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_planif.bat
```

### Grafana
Access Grafana in your browser by going to localhost:3000.

If the service is running, you will be prompted to log in (admin:admin).

In the bottom-left, go to Administration > Data sources.

Create a MYSQL data source and fill in the connection information.
![sql](https://github.com/vampi62/coccapitalwatch/assets/104321401/d6cfc9a9-df56-428f-9e00-a20069dbbe42)

Click on "Save & Test."

In the dashboard, click on "New" > "Import."

Import the coccapitalwatch-xxxx.json dashboard.
Change the time display to UTC.
![utc](https://github.com/vampi62/coccapitalwatch/assets/104321401/20367ef6-ecbb-4f06-824e-f5d276e442c7)

## Installation on Linux

### Download
https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/

```sh
sudo apt install python
sudo apt install mariadb-server
```

### Python module
```sh
pip install requests
pip install mysql-connector-python
```

### SQL database configuration
```sh
sudo mysql -u root -p
```
```sh
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('NewPassword');
FLUSH PRIVILEGES;
exit
```

### Optional Discord bot
If you want to use the Discord bot:
```sh
pip install discord
```

On the Discord website https://discord.com/developers/applications:
- Create an application
- Create a bot
- Add the "message content intent" permission in the "Bot" menu
- Copy the token
- Connect the bot to your Discord server (the bot should have "read message," "send message," "read message history," and "send messages in threads" permissions)
- Copy the channel ID where you want the bot to post messages.

### Configuring the config.json file
Complete the config.json file:
- bdip: the IP address of your database
- bdport: the port of your database
- bduser: the database user
- bdpass: the database password

- bdname: the name of your database
- api_key: your Clash of Clans API key
- clan_tag: the ID of the clan to monitor
- discord_token: the Discord bot token (leave empty if not using Discord)
- discord_channel: the channel ID where you want the bot to post messages (leave empty if not using Discord)
- lang: fr or en

### Configuring the SQL table
Run the database installation script (change the directory if necessary):
```sh
python C:/Téléchargements/coccapitalwatch/install/install_db.py
```

### Service on Windows

- Install the service or scheduled task depending on whether you are using Discord or not:
Service if using Discord:
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_service.bat
```
Scheduled task if not using Discord:
```sh
python C:/Téléchargements/coccapitalwatch/install/install_windows_planif.bat
```

### Grafana
Access Grafana in your browser by going to localhost:3000.

If the service is running, you will be prompted to log in (admin:admin).

In the bottom-left, go to Administration > Data sources.

Create a MYSQL data source and fill in the connection information.
![sql](https://github.com/vampi62/coccapitalwatch/assets/104321401/d6cfc9a9-df56-428f-9e00-a20069dbbe42)

Click on "Save & Test."

In the dashboard, click on "New" > "Import."

Import the coccapitalwatch-xxxx.json dashboard.
Change the time display to UTC.
![utc](https://github.com/vampi62/coccapitalwatch/assets/104321401/20367ef6-ecbb-4f06-824e-f5d276e442c7)

## Installation on Linux

### Download
https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/

```sh
sudo apt install python
sudo apt install mariadb-server
```

### Python module
```sh
pip install requests
pip install mysql-connector-python
```

### SQL database configuration
```sh
sudo mysql -u root -p
```
```sh
CREATE DATABASE coc;
CREATE USER 'coc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON coc.* TO 'coc'@'localhost';
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('NewPassword');
FLUSH PRIVILEGES;
exit
```

### Optional Discord bot
If you want to use the Discord bot:
```sh
pip install discord
```

On the Discord website https://discord.com/developers/applications:
- Create an application
- Create a bot
- Add the "message content intent" permission in the "Bot" menu
- Copy the token
- Connect the bot to your Discord server (the bot should have "read message," "send message," "read message history," and "send messages in threads" permissions)
- Copy the channel ID where you want the bot to post messages.

### Configuring the config.json file
Complete the config.json file:
- bdip: the IP address of your database
- bdport: the port of your database
- bduser: the database user
- bdpass: the database password
- bdname: the name of your database
- api_key: your Clash of Clans API key
- clan_tag: the ID of the clan to monitor
- discord_token: the Discord bot token (leave empty if not using Discord)
- discord_channel: the channel ID where you want the bot to post messages (leave empty if not using Discord)
- lang: fr or en

### Configuring the SQL table
Run the database installation script (change the directory if necessary):
```sh
python ~/coccapitalwatch/install/install_db.py
```

### Service on Linux
Install the service or scheduled task depending on whether you are using Discord or not:
Service if using Discord:
```sh
python ~/coccapitalwatch/install/install_linux_service.sh
```
Scheduled task if not using Discord:
```sh
python ~/coccapitalwatch/install/install_linux_planif.sh
```

### Grafana
Access Grafana in your browser by going to localhost:3000.

If the service is running, you will be prompted to log in (admin:admin).

In the bottom-left, go to Administration > Data sources.

Create a MYSQL data source and fill in the connection information.
![sql](https://github.com/vampi62/coccapitalwatch/assets/104321401/d6cfc9a9-df56-428f-9e00-a20069dbbe42)

Click on "Save & Test."

In the dashboard, click on "New" > "Import."

Import the coccapitalwatch-xxxx.json dashboard.
Change the time display to UTC.
![utc](https://github.com/vampi62/coccapitalwatch/assets/104321401/20367ef6-ecbb-4f06-824e-f5d276e442c7)


## Clan Hall Monitoring

If you are not using the Discord service, you can monitor the state of the Hall by inserting values into the database. To do this:

- Execute inserthall.py to add a measurement of the Hall's state. In the game, get the number of gems invested in the Hall and enter this value in the input area.

After inserting this value into the database, the script will compare the difference between this value and the last recorded value to find the deposits responsible for this change.

```sh
python insertall.py
```

Example in the attached images.

![2hall](https://github.com/vampi62/coccapitalwatch/assets/104321401/184a5306-998f-4e2c-90ec-5b0c638399af)

![correspondance](https://github.com/vampi62/coccapitalwatch/assets/104321401/1936c7bb-bc0b-45b4-ad74-8fe62286b9af)

If you are using the Discord service, enter the value in the Discord channel where the bot posts messages:

- /insert __hall_value__ -- to insert a value and get the details of the deposits responsible for this change

- /reset 0 -- to reset the Hall's counter to 0

## Uninstallation

### Windows Service

Execute the corresponding uninstall_ file for your installation:

__os_used__: windows or linux

__service_or_schedule__: service or planif (service if using Discord, otherwise planif)

/coccapitalwatch/install/uninstall_ __os_used__ _ __service_or_schedule__