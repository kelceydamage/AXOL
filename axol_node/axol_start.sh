#! /bin/bash

echo -e "\e[1;44m Running Processes Before                         \e[0m\n"
ps aux|grep celery
echo ""

for line in $( pgrep python )
do
        echo -e "\e[1;31m Killing PID: $line\e[0m"
        kill -9 $line
done

echo -e "\n\e[44m Stopping AXOL-ML                           [\e[1;32mDONE\e[0m\e[44m]\e[0m\n"

echo -e "\e[1;44m Running Processes After                          \e[0m\n"
ps aux|grep celery

sudo chown axol:axol /opt/AXOL_Management/AXOL/axol_node/database
sudo chown axol:axol /var/log/celery
sudo chown axol:axol /var/run/celery
echo -e "\n\e[44m Setting Up Permissions                     [\e[1;32mDONE\e[0m\e[44m]\e[0m"

#sudo rm -rf /opt/AXOL_Management/AXOL/axol_node/database/*.mdb
echo -e "\e[44m Clearing Old Snapshot Data                 [\e[1;32mDONE\e[0m\e[44m]\e[0m\n"


service celeryd restart
service apache2 restart
echo -e "\n\e[44m Starting AXOL-ML                           [\e[1;32mDONE\e[0m\e[44m]\e[0m"

sudo chown axol:www-data /opt/AXOL_Management/AXOL/axol_node/database/*
sudo chmod 775 /opt/AXOL_Management/AXOL/axol_node/database/*
echo -e "\e[44m Setting Database Permissions               [\e[1;32mDONE\e[0m\e[44m]\e[0m\n"

echo -e "\e[1;44m Program Status                                   \e[0m"
echo -e "\e[1;32m#------------------------------------------------#\e[0m"
service celeryd status
service apache2 status
echo -e "\e[1;32m#------------------------------------------------#\e[0m\n"
