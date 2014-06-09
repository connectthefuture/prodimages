#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################
import mechanize, cookielib
import os,sys,re

class MyBrowser(mechanize.Browser, object):

    def __init__(self):
        super(MyBrowser, self).__init__()
        
        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cj)
        # Opts
        self.set_debug_http(True)
        self.set_debug_redirects(True)
        self.set_debug_responses(True)
        self.set_handle_equiv(True)
        self.set_handle_gzip(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        #self.set_proxies({"http" : "http://proxy.me.com:80"})

        # Follows refresh 0 but not hangs on refresh > 0
        self.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # HTTP Headers to Pass in request -- Uncomment no more than 1 of each
        
        # Accept
        #self.addheaders = [('Accept', 'text/html')]
        #self.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
        
        # Content
        self.addheaders = [('Content-Type', 'text/html')]
        #self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        #self.addheaders = [('Content-length', '{0}'.format(str(len(data))))]
        
        # User-Agent 
        # self.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0')]

        

from BeautifulSoup import MinimalSoup 
class PrettifyHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = MinimalSoup(response.get_data())
            response.set_data(soup.prettify())
        return response


class VpnbflyMyBrowser(MyBrowser, PrettifyHandler):
    def __init__(self):
        super(VpnbflyMyBrowser, self).__init__()
        self.uname        = ''
        self.pword        = ''
        self.url_login_vpn         = 'https://vpn.bluefly.com/login.html'
        self.url_login_cgi         = 'https://vpn.bluefly.com/dana-na/auth/url_0/welcome.cgi'
        self.url_login_bypass_JSAM = 'https://vpn.bluefly.com/dana/home/starter.cgi?startpageonly=1'
        self.url_login_pm          = 'https://pm.bluefly.corp/login.html'
        self.url_login_vpnpm       = 'https://vpn.bluefly.com/manager/,DanaInfo=pm.bluefly.corp+login.html'
        self.url_logout_vpn        = 'https://vpn.bluefly.com/dana-na/auth/logout.cgi'

        # Set Global Style number variable if available in env
        try:
            self.style = style
        except:
            self.style = ''
            pass
        
        self.url_proddesc   = self.get_url_proddesc    
        self.url_vpnproddesc = self.get_url_vpnproddesc


    def login_vpn(self):
        """Login to Remote VPN network with auth"""
        self.open(self.url_login_vpn)
        self.select_form(nr=0)
        self.form['username'] = self.uname
        self.form['password'] = self.pword
        
        # Referer 
        self.addheaders = [('Referer', 'https://vpn.bluefly.com/login.html')]
        # Content Type is form
        self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        
        self.submit()
        self.open(self.url_login_bypass_JSAM)
        
        ## Confirm if Confirm Required
        #self.select_form(nr=0)
        #if self.form.name == 'frmConfirmation':
        #    self.submit()
        #else:
        #    print self.form.name 
            #return [ self.form.name for self.form in self.forms ]
           
    def login_pm_vpn(self):
        """Login to pm when logged on to remote vpn network"""

        self.open(self.url_login_vpnpm)

        self.select_form(nr=0)
        self.form['j_username'] = self.uname
        self.form['j_password'] = self.pword
        # Referer 
        self.addheaders = [('Referer', '{0}'.format(self.url_login_vpnpm))]
        # Content Type is form
        self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        self.submit()

    def login_pm(self):
        """Login to pm when on local bfly network"""
        self.open(self.url_login_pm)
        
        self.select_form(nr=0)
        self.form['j_username'] = self.uname
        self.form['j_password'] = self.pword       
        # Referer 
        self.addheaders = [('Referer', '{0}'.format(self.url_login_pm))]
        # Content Type is form
        self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]        
        self.submit()
    
    # Logout Vpn
    def logout_vpn(self):
        """Login out from vpn remote"""
        self.open(self.url_logout_vpn)
    
    # Generate Pm Product Detail URL when Passed self.style ( for self.style in style_list: self.get_url_proddesc()    ) or style?not sure
    def get_url_proddesc(self):
        self.pmurl_style    = "https://pm.bluefly.corp/productdetails.html?id={0}".format(self.style)
        return self.pmurl_style
    
    def get_url_vpnproddesc(self):
        self.vpnpmurl_style = "https://vpn.bluefly.com/manager/product/,DanaInfo=pm.bluefly.corp+productdetails.html?id={0}".format(self.style)
        return self.vpnpmurl_style
        
    def submit_save_proddesc(self):
        """ Plug a list of styes to go to om prddeet page and submit save"""
        self.login_pm_vpn()
        _proddesc_style_url = self.get_url_proddesc()
        self.open(_proddesc_style_url)
        
        ## Preprocess Response to Account for Bad HTML         
        _response = self.response() 
        headers = _response.info()  
        headers['Referer'] = '{0}'.format(_proddesc_style_url)
        headers["Content-type"] = "text/html; charset=utf-8"
        
        _response.set_data(_response.get_data().replace("<!---", "<!--"))
        self.set_response(_response)
        self.select_form(name='editProductDetailsForm')
        self.submit()



##################################
########### XTRA #################

def prddesc_url_list(styles):
    styleurls_pmdesc = []
    for style in styles:
        pmdesc = anewbasic.get_url_vpnproddesc()
        styleurls_pmdesc.append(pmdesc)
    return styleurls_pmdesc

##################################
##################################


##################################
############ RUN #################
##################################
def main():
    loginer = VpnbflyMyBrowser()
    res = loginer.login_vpn()
    return res


if __name__ == '__main__':
    print main()
