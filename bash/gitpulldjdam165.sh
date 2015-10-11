#!/bin/bash

. ~/.bash_profile

PWD=/home/johnb/vm/DJDAM/djdam

echo `date` >> ~/.djdam165.log

cd /home/johnb/vm/DJDAM/djdam && git pull origin master >> ~/.djdam165.log


