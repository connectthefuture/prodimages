#!/bin/bash

. ~/.bash_profile

PWD=/usr/local/batchRunScripts/offshore_image_processes

echo `date` >> ~/.offshoreprocsgit.log

cd /usr/local/batchRunScripts/offshore_image_processes && git pull origin master >> ~/.offshoreprocsgit.log


