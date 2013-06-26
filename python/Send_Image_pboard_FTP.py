##### Takes Image on Pasteboard from Iphone and saves via FTP a 600px image to Dropbox Returns a link to iPhone sized image to view

import Image, ImageOps, ImageFilter
import ftplib
import console
import clipboard
import datetime
from io import BytesIO
import urllib

today = datetime.datetime.now()
image = clipboard.get_image()
fileName = console.input_alert("Image Title", "Enter Image File Name")
fileName = fileName + '_' + today.strftime("%Y-%m-%d-%H%M%S") + '.png'

userName = "myUserName"
userPass = "myPassWord"
host = "prodjohn8.bluefly.corp"
port = 22
urlBase = "http://192.168.21.111:8082/Dropbox_sites/SpyderMac/py_iphone/uploads_from_iphone"

remotePath = "/Users/johnb/Dropbox_sites/SpyderMac/py_iphone/uploads_from_iphone"

datePath = today.strftime("%Y/%m/")
# Used to create full remote file path
remoteFilePath =  remotePath + datePath

def customSize(img):
    w, h = img.size
    print 'w: ' + str(w)
    print 'h: '+ str(h)
    if w > 600:
        wsize = 600/float(w)
        print 'wsize: '+str(wsize)
        hsize = int(float(h)*float(wsize))
        print 'hsize: ' + str(hsize)

        img = img.resize((600, hsize), Image.ANTIALIAS)
    return img

image = customSize(image)
print image.size
image.show()

buffer = BytesIO()
image.save(buffer, 'PNG')
buffer.seek(0)

print remoteFilePath
print fileName

fileURL = urllib.quote(fileName)

ftp = ftplib.FTP(host, userName, userPass)
ftp.cwd(remoteFilePath)
ftp.storbinary('STOR '+fileName, buffer)
ftp.quit()
imageLink = urlBase+datePath+fileURL
print(imageLink)
clipboard.set(imageLink)
