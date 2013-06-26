#!/bin/bash
. ~/.bash_profile



rsync -avz $pushStill $archStill & rsync -avz $pushFashion $archFashion \;

exit;
