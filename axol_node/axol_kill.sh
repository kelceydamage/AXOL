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
