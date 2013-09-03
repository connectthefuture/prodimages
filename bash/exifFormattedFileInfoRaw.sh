 #!/bin/bash
. ~/.bash_profile
. ~/.bashrc

sourceDir=$1
TODAY=$(date +"%m-%d-%Y")
FormatFile=$PRODSRV/lib/exifFormatFilePrdStats_ex.txt


exiftool -d %d-%b-%Y -m -f -r -p ${FormatFile} ${sourceDir} > ~/''${TODAY}'_MetaDateReport_'By'-'${USER}''

exit;