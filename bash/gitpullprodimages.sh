#!/bin/bash

. ~/.bash_profile

PWD=/usr/local/batchRunScripts

echo `date` >> ~/.prodimagesgit.log

cd /usr/local/batchRunScripts && git pull origin revert_ready >> ~/.prodimagesgit.log
