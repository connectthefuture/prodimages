#!/bin/bash
. ~/.bash_profile



rsync -CtavzP ${pushStill} ${archStill} & rsync -CtavzP ${pushFashion} ${archFashion} \;

exit;
