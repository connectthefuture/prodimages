#!/bin/bash

. ~/.bash_profile

PWD=/home/johnb/virtualenvs/DAMNATION/src

. $PWD/../bin/activate

echo `date` >> ~/.damnationgit.log


cd /home/johnb/virtualenvs/DAMNATION/src && git pull damorigin master >> ~/.damnationgit.log

sleep 7

test=`tail -1 ~/.damnationgit.log`

if [ "$test" == "Already up-to-date." ]; then
echo "Nothing to Do"
else
# echo "ELSE"
cd /home/johnb/virtualenvs/DAMNATION/src && source ../bin/activate ## && python $PWD/manage.py syncdb --migrate >> ~/.damnation.log
fi;





