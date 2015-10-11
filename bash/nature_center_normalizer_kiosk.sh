#!/bin/bash

. ~/.bash_profile

export PWD=/mnt/Post_Complete/Complete_to_Load/nature_center
echo "`date`_`pwd`" >> ~/.naturecenter.log


regex_matcherator_matched=`python -c '''
def main(dname=None):
    import os.path
    import glob
    dname = os.path.abspath(dname)
    destdir = os.path.abspath(os.path.join(dname, '../output'))
    fpaths = glob.glob(os.path.join(dname, '*/*.*'))
    ##destdir, dname
    for fpath in fpaths:
        ##retoutput = run_imgconv_function(fpath,destdir)
        scriptname = os.path.dirname(fpath).split('/')[-1]
        dest = os.path.join(destdir, scriptname)
        print fpath, dest ;

main(dname="\$f");'''`


if [ "$regex_matcherator_matched" == "" ]; then
echo "NothingToDo `date`_`pwd`" > ~/.naturecenter.log
else
# echo "ELSE"
for f in regex_matcherator_matched; do
    some_image_func "$f" ;
    echo "SomethingsBeenDone `date`_${f}" > ~/.naturecenter.log
done;
fi;
