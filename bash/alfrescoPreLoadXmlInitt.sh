#!/bin/bash
. ~/.bash_profile
. ~/.bashrc
loggerX=`date >> ~/Dropbox/logger.txt`
echo $loggerX
#dirStill="/mnt/Post_Ready/Retouch_Still/"
#dirFashion="/mnt/Post_Ready/Retouch_Fashion/"
#filesStill7=`find /mnt/Post_Ready/Retouch_Still/ -type f -mtime -7 -iname \*.jpg`
#filesFashion7=`find /mnt/Post_Ready/Retouch_Fashion/ -type f -mtime -7 -iname \*.jpg`
#importArgs="$@"
#for f in "$@"
importDir=/mnt/Post_Ready/zAlfresco_Primary/Alfresco_Batch_Import/
importDirFiles=`find $importDir -type f -iname \*.jpg`
tmpImportDirInPrg=/mnt/Post_Ready/zAlfresco_Primary/tmp_Alfresco_Batch_Import_Drop
tmpImportDirComplete=/mnt/Post_Ready/zAlfresco_Primary/tmp_Alfresco_Batch_Import_Complete
exifXmlFmt=$LIBSRV/exifFormatFile_XML_AlfAltered.txt

for f in $importDirFiles
do
outName=`basename "$f" | sed s/.jpg//g`
xmlOutImport="$tmpImportDirInPrg/$outName.jpg.metadata.properties.xml"
#exiftool -X -E -f -m -l -listItem 0 -struct -p $exifXmlFmt $f > $xmlOutImport
exiftool -d +%D-%b-%y -ee -m -f -p $exifXmlFmt $f > $xmlOutImport
mv $f $tmpImportDirInPrg
done;

###    #   <-------copy of file and xmlShadow sent to sort. jpg is rezed down to 600x720
   #   Sort to dir hashs
cd $tmpImportDirInPrg
for f in `find $tmpImportDirInPrg -type f -maxdepth 1 -iname \*.*`
do
outNameFull=`basename "$f"`
exiftool -'directory'=$tmpImportDirInPrg/%4f/ $tmpImportDirInPrg/$outNameFull
#exiftool -f -'directory'=$importDir/%4f/ $xmlOutImport
#mv $f $tmpImportDirComplete
#cd $tmpImportDirComplete
#exiftool -'directory'=$tmpImportDirComplete/%4f/ $tmpImportDirComplete/$outName.jpg
done;
echo $loggerX
exit;
