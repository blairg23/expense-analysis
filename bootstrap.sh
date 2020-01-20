#!/bin/bash
echo
echo "Expensive Bootstrap v2.0"

echo "- Updating apt-get"
sudo apt-get update
sudo apt-get upgrade

#echo -n "- Making sure we have mysql-server installed."
#sudo apt-get install mariadb-server
#sudo apt-get install mariadb-client
#sudo apt-get install libmysqlclient-dev
#echo " Done"

#echo -n "- Cleaning up any databases that already exist and recreating:"
#mysqladmin --user=root --password=tomis_admin2016 drop expensive
#mysql --user=root --password=tomis_admin2016 -e "CREATE DATABASE expensive CHARACTER SET latin1 COLLATE latin1_general_ci;"
#echo " Done"

echo -n "- Cleaning up any migrations that already exist:"
# rm tomis
rm db.sqlite3
rm debug.log
find . -type f -name '[0-9][0-9][0-9][0-9]*.py' -delete > /dev/null 2>&1
rm -r `find . -type d -name '__pycache__'` > /dev/null 2>&1
py3clean .
echo " Done"

echo "- Making sure we have the python development libraries installed"
sudo apt-get install python3-dev > /dev/null
echo " Done"

#echo "- Making sure we have the mysqlclient-dev dependencies."
#sudo apt-get install libmysqlclient-dev
#echo " Done"

echo -n "- Installing requirements:"
pip3 install -r requirements.txt --upgrade #> /dev/null 2>&1
echo " Done"

echo -n "- Bootstrapping the database with some basic information:"
./manage.py makemigrations #> /dev/null 2>&1
./manage.py migrate #> /dev/null 2>&1

#
# Base system data
#
./manage.py loaddata expensive/fixtures/01_sites.json
./manage.py loaddata expensive/fixtures/02_users.json

echo " Done"

echo "Basics done, do a ./manage.py runserver to run the development django server locally"
echo "Admin Username: admin@expensive"
echo "Admin Password: i had a dreamst"