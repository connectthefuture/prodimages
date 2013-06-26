#class uploadfromfile:
#    def POST(self, name=None):
#        filename = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
#        i in range(20)
#        x = web.input(upfile={})
#        f = open(filename, 'wb')
#        f.write(x['upfile'].value)
#        f.close()
#        (filename)
#        return "some html"
    


import web

urls = (
    '/', 'index'
)

class index:
    
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



class download:

   def GET(self, args):
       path = 'path/to/image' 
       web.header('Content-type','images/jpeg')
       web.header('Content-transfer-encoding','binary') 
       web.header('Content-Disposition', 'attachment;filename="fname.ext"')
       return open(path, 'rb').read()




###Start the server
### If you go to your command line and type:

## python code.py
### http://0.0.0.0:8080/


