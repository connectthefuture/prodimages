#!/bin/bash

uploadDropbox=/mnt/johnb/Dropbox/Retouchers-Remote-Upload

jamesDone=/mnt/johnb/Public/Drop_FinalFilesOnly/JamesHoetker
jamesFind=`find $uploadDropbox -iname \*jh\*.zip`
unzip -j -u -o -qq $jamesFind -d $jamesDone
rm $jamesFind

jenDone=/mnt/johnb/Public/Drop_FinalFilesOnly/JenFolks
jenFind=`find $uploadDropbox -iname \*jf\*.zip`
unzip -j -u -o -qq $jenFind -d $jenDone
rm $jenFind

johnDonne=/mnt/johnb/Public/Drop_FinalFilesOnly/JohnBragato
johnFind=`find $uploadDropbox -iname \*jb\*.zip`
unzip -j -u -o -qq $johnFind -d $johnDonne
rm $johnFind

nicoleDone=/mnt/johnb/Public/Drop_FinalFilesOnly/NicoleCraine
nicoleFind=`find $uploadDropbox -iname \*nc\*.zip`
unzip -j -u -o -qq $nicoleFind -d $nicoleDone
rm $nicoleFind

stephenDone=/mnt/johnb/Public/Drop_FinalFilesOnly/StephenParker
stephenFind=`find $uploadDropbox -iname \*sp\*.zip`
unzip -j -u -o -qq $stephenFind -d $stephenDone
rm $stephenFind

#######		Freelance 1 and 2
freelance1Done=/mnt/johnb/Public/Drop_FinalFilesOnly/xFreelance_One
freelance1Find=`find $uploadDropbox -iname \*free1\*.zip`
unzip -j -u -o -qq $freelance1Find -d $freelance1Done
rm $freelance1Find

freelance2Done=/mnt/johnb/Public/Drop_FinalFilesOnly/xFreelance_Two
freelance2Find=`find $uploadDropbox -iname \*free2\*.zip`
unzip -j -u -o -qq $freelance2Find -d $freelance2Done
rm $freelance2Find

exit;
