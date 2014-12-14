#!/bin/bash

. ~/.bash_profile

PWD=/home/imageman/virtualenvs/DJMONGO/src

. "$PWD"/../bin/activate

echo `date` >> ~/.djmongogit.log


cd /home/imageman/virtualenvs/DJMONGO/src && git pull origin master >> ~/.djmongogit.log

sleep 7

test=`tail -1 ~/.djmongogit.log`

if [ "$test" == "Already up-to-date." ]; then
echo "Nothing to Do"
else
# echo "ELSE"
cd /home/imageman/virtualenvs/DJMONGO/src && source ../bin/activate ## && python $PWD/manage.py syncdb --migrate >> ~/.mongodj.log
fi;





