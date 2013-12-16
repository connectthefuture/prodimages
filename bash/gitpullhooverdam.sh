#!/bin/bash

. ~/.bash_profile


PWD=/home/johnb/virtualenvs/HOOVERDAM/src

. $PWD/../bin/activate

echo `date` >> ~/.githooverdam.log


cd /home/johnb/virtualenvs/HOOVERDAM/src && git pull origin master >> ~/.githooverdam.log

sleep 7

test=`tail -1 ~/.githooverdam.log`

if [ "$test" == "Already up-to-date." ]; then
echo "Nothing to Do"
else
# echo "ELSE"
cd /home/johnb/virtualenvs/HOOVERDAM/src && source ../bin/activate ## && python $PWD/manage.py syncdb --migrate >> ~/.damnation.log
fi;





