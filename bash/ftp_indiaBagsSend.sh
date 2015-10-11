#!/bin/bash

FtpHostUp = "file3.bluefly.corp"
FtpPathUp = "/ImageDrop/"
FtpHostDn = "netsrv101.l3.bluefly.com/" as string
FtpPathDn = "/mnt/images/images/" as string
FtpUser = "imagedrop"
FtpPass = "BLU1002wet"
FtpPort = "23" as text
HttpsUrl = "https://imagedrop:imagedrop0@file3.bluefly.corp/ImageDrop/"




curl -G ftp://netsrv101.l3.bluefly.com//mnt/images/images/3187/318706801.png --user imagedrop:imagedrop0 -o ~/Pictures/318706801.png


curl -G ftp://prepressoutsourcing.com/318706801.png --user blu:BLU1002wet -o ~/Pictures/318706801.png
