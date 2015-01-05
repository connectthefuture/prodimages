#!/bin/bash
. ~/.bash_profile

RUNFILE="$1"
RUNFILEARG1="$2"
PROCNAME=`basename "$RUNFILE" | sed 's/.py//g'` 
LOCKFILE=/tmp/"$PROCNAME"_lock

if [ -f "$LOCKFILE" ]
then
    echo "Lockfile exists, process currently running."
    echo "If no processes exist, remove $LOCKFILE to clear."
    echo "Exiting..."
mailx -s "AUTOMATED - ${PROCNAME} LOCK ERROR" john.bragato@bluefly.com <<+ Lockfile exists, process currently running.
If no processes exist, remove $LOCKFILE to clear.
+
exit
fi

## Make LOCKFILE if not exists
touch "$LOCKFILE"

#### Run Script passed as 1st arg
python "$RUNFILE" "$RUNFILEARG1"

echo "DONE ${PROCNAME}"
## Remove the LOCKFILE allowing process to run again
rm "$LOCKFILE"

