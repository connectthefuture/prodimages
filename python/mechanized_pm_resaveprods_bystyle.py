import mechanize
import cookielib
import os,sys,re,glob

url = sys.argv[1]

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

pmstyle_urls = []
vpnpmstyle_urls = []
styles_list = ['336407001','336406101','336404301','336403901','336403501','336403301','336401501','336401001','336359101','336358901','336249301','336249101','336186901','335742901','335742801','335742701','335742301','325497201']

for style in styles_list:
    pmurl_style    = "https://pm.bluefly.corp/productdetails.html?id={0}".format(style)
    pmstyle_urls.append(pmurl_style)
    vpnpmurl_style = "https://vpn.bluefly.com/manager/product/,DanaInfo=pm.bluefly.corp+productdetails.html?id={0}".format(style)
    vpnpmstyle_urls.append(vpnpmurl_style)


## Login
uname = 'johnb'
pword = '$cutler2377'
pmurl_login = 'https://pm.bluefly.corp/login.html'

def login_pm(url):
    pm_login = br.open(url)
    br.select_form('frmLogin')
    
    
class BrowserSecureSessBrowser(mechanize.Browser):
    import sys, mechanize, os
    
    def __init__(self):
        self.uname = uname
        self.pword = pword
        self.url   = url 
        self.br    = browser_init
        
    
    def browser_init(self):
        # Browser
        self.br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)

        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #self.br.set_debug_http(True)
        #self.br.set_debug_redirects(True)
        #self.br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        
        return self.br
      
    def login(self):
        
        return self


#############
import mechanize
class MyBrowser(mechanize.Browser, object):
    _username   = 'johnb'
    _password   = '$cutler2377'
    _loginurl   = 'https://vpn.bluefly.com/dana-na/auth/url_0/welcome.cgi'
    _pmloginurl = 'https://vpn.bluefly.com/login.html'
    
    
    def __init__(self):
        super(MyBrowser, self).__init__()
        self.set_handle_robots(False)
        self.set_proxies({"http" : "http://proxy.me.com:80"})
        self.set_handle_equiv(True)
        self.set_handle_gzip(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        self.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    
    def login_vpn(self):
        self.open(self._loginurl)
        self.select_form(nr=0)
        super(MyBrowser, self)._username = _username
        super(MyBrowser, self)._password = _password
        self.submit()
    
    def login_pm(self):
        self.open(self._pmloginurl)
        self.select_form(nr=0)
        self._username = _username
        self._password = _password
        br.open(self.url)
        for form in br.forms():
            if form.name == form_to_get:
                save_style_form = br.select_form(self.form_to_get)
        self.submit()
        
    def pm_url(self):
        self.pmurl_style    = "https://pm.bluefly.corp/productdetails.html?id={0}".format(style)
        return self.pmurl_style
    
    def vpnpm_url(self):
        self.vpnpmurl_style = "https://vpn.bluefly.com/manager/product/,DanaInfo=pm.bluefly.corp+productdetails.html?id={0}".format(style)
        return self.vpnpmurl_style

###############
class PMSecureSessBrowser(BrowserSecureSessBrowser):
    
    def __init__(self):
        self.uname = self.BrowserSecureSessBrowser
        self.pword = sys.argv[2]
        self.url   = 'https://pm.bluefly.corp/login.html'    
        self.form_to_get = 'editProductDetailsForm'
        
    def save_pmstyle(self):
        
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.open(self.url)
        for form in br.forms():
            if form.name == form_to_get:
                save_style_form = br.select_form(self.form_to_get)
                #save_style_form =     
    


import mechanize
import cookielib

class MyBrowser(mechanize.Browser, object):

    def __init__(self):
        super(MyBrowser, self).__init__()
        
        
        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cj)
        # Opts
        self.set_handle_robots(False)
        self.set_proxies({"http" : "http://proxy.me.com:80"})
        self.set_handle_equiv(True)
        self.set_handle_gzip(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        self.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # User-Agent 
        self.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        



class VpnbflyMyBrowser(MyBrowser):
    def __init__(self):
        super(VpnbflyMyBrowser, self).__init__()
        self.uname        = 'johnb'
        self.pword        = '$cutler2377'
        self.url_login_base = 'https://vpn.bluefly.com/login.html'
        self.url_login_cgi  = 'https://vpn.bluefly.com/dana-na/auth/url_0/welcome.cgi'
        self.url_pmlogin    = 'https://pm.bluefly.corp/login.html'
        
        # Set Global Style number variable if available in env
        try:
            self.style        = style
        except:
            pass
        
        self.url_proddesc   = self.get_url_proddesc    
        self.url_vpnproddesc = self.get_url_vpnproddesc

    def login_vpn(self):
        self.open(self.url_login_base)
        self.select_form(nr=0)
        
        #super(VpnbflyMyBrowser, self).
        self.form.controls[1] = self.uname
        self['username'] = self.uname
        #super(VpnbflyMyBrowser, self)
        self.form.controls[2] = self.pword
        self['password'] = self.pword
        self.submit()
    
    def login_pm(self):
        self.open(self._loginurl)
        self.select_form(nr=0)
        super(MyBrowser, self).self.uname = self.uname
        super(MyBrowser, self).self.pword = self.self.pword
        self.submit()
        
    def get_url_proddesc(self):
        self.pmurl_style    = "https://pm.bluefly.corp/productdetails.html?id={0}".format(self.style)
        return self.pmurl_style
    
    def get_url_vpnproddesc(self):
        self.vpnpmurl_style = "https://vpn.bluefly.com/manager/product/,DanaInfo=pm.bluefly.corp+productdetails.html?id={0}".format(self.style)
        return self.vpnpmurl_style
## VPN FORM ELEMENT NAMES
#br.form['username'] = uname
#br.form['password'] = pword

## PM FORM ELEMENT NAMES FOR LOGIN
br.form['j_username'] = uname
br.form['j_password'] = pword
        
response = br.submit()
response.read()

br.close()

