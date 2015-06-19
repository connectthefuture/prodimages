
#!/bin/bash
# echo-params.sh

# Call this script with a few command-line parameters.
# For example:
#     sh echo-params.sh first second third fourth fifth

params=0              # Number of command-line parameters.
param=1                # Start at first command-line param.

while [  -le  ]
do
  echo -n Command-line parameter 
  echo -n $     #  Gives only the *name* of variable.
#         ^^^          #  , , , etc.
                       #  Why?
                       #  $ escapes the first 
                       #+ so it echoes literally,
                       #+ and  dereferences  . . .
                       #+ . . . as expected.
  echo -n  = 
  eval echo $   #  Gives the *value* of variable.
# ^^^^      ^^^        #  The eval forces the *evaluation*
                       #+ of $$
                       #+ as an indirect variable reference.

(( param ++ ))         # On to the next.
done

exit 1
