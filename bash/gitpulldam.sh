#!/bin/bash

. ~/.bash_profile

PWD=/home/johnb/virtualenvs/DJDAM/src

. $PWD/../bin/activate

echo `date` >> ~/.djdamgit.log


cd /home/johnb/virtualenvs/DJDAM/src && git pull origin master >> ~/.djdamgit.log

sleep 7

test=`tail -1 ~/.djdamgit.log`

if [ "$test" == "Already up-to-date." ]; then
echo "Nothing to Do"
else
# echo "ELSE"
cd /home/johnb/virtualenvs/DJDAM/src && source ../bin/activate ## && python $PWD/manage.py syncdb --migrate >> ~/.djdamgit.log
fi;


# echo `env` >> ~/.djdamgit.log


