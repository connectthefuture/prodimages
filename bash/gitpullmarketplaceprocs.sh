#!/bin/bash

. ~/.bash_profile

PWD=/usr/local/batchRunScripts/prodimages-ny

echo `date` >> ~/.marketplaceprocsgit.log

cd /usr/local/batchRunScripts && git pull origin master >> ~/.marketplaceprocsgit.log
