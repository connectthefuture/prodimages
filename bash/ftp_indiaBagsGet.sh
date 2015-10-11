#!/bin/bash

#ftp://blu@prepressoutsourcing.com/Drop/Bags/
#ftp://blu@prepressoutsourcing.com/Pick/Bags_Done/

FtpHostUp = "prepressoutsourcing.com"
FtpPathUp = "Drop/Bags"
FtpHostDn = "prepressoutsourcing.com"
FtpPathDn = "Pick/Bags_Done"
FtpUser = "blu"
FtpPass = "BLU1002wet"
FtpPort = "23"
HttpsUrl = "https://$FtpUser:$FtpPass@$FtpPathUp/$FtpPathUp/"
FtpFileName = $1
FtpFilePath = $2
LocalImageSendDir= "/mnt/Post_Ready/Retouchers/Handbags/Send"
LocalImageReturnDir= "/mnt/Post_Ready/Retouchers/Handbags/Ready"


curl -G ftp://$FtpHostDn/$FtpPathDn/$FtpFile --user $FtpUser:$FtpPass -o $LocalImageReturnDir/$FtpFile

ftp://blu@prepressoutsourcing.com/Pick/06-SEP-2012_Done/



" --user blu:BLU1002wet -o "



357462601