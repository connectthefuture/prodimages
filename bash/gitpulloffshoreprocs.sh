#!/bin/bash

. ~/.bash_profile

PWD=/usr/local/batchRunScripts/offshore-processes

echo `date` >> ~/.offshoreprocsgit.log

cd /usr/local/batchRunScripts/offshore-processes && git pull origin master >> ~/.offshoreprocsgit.log


