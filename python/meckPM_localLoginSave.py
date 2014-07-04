#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mechanize, cookielib
import os,sys,re,glob

class MyBrowser(mechanize.Browser, object):

    def __init__(self):
        super(MyBrowser, self).__init__()
        
        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cj)
        # Browser Opts
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
            soup = MinimalSoup (response.get_data())
            response.set_data(soup.prettify())
        return response


class PMbflyMyBrowser(MyBrowser, PrettifyHandler):
    def __init__(self):
        super(PMbflyMyBrowser, self).__init__()
        self.uname              = '{}'.format(str(input('Enter your username: ')))
        self.pword              = '{}'.format(str(input('Enter your password: ')))
        self.url_login_pm       = 'http://pm.bluefly.corp/manager/login.html'
        self.url_logout_pm      = 'http://pm.bluefly.corp/manager/logout.html'
        # Set Global Style number variable if available in env
        try:
            self.style = style
        except:
            self.style = ''
            pass
        
        self.url_proddesc   = self.get_url_proddesc()    

        #self.url_prodmerge    = self.get_url_prodmerge()    
    
    
    ## LOGIN LOGOUT SECTION
    def login_pm(self):
        ## Login to pm when on local bfly network
        self.open(self.url_login_pm)
        self.select_form(nr=0)
        #self.select_form('frmLogin')
        self.form['j_username'] = self.uname
        self.form['j_password'] = self.pword
        # self.form['action']     = 'j_acegi_security_check'
        #for form in self.forms():
        #    if form.action == self.form['action']:
        #save_style_form = self.select_form(self.form_to_get)       
        # Referer 
        self.addheaders = [('Referer', '{0}'.format(self.url_login_pm))]
        
        # Content Type is form
        self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        self.submit()


    def logout_pm(self):
        self.open(self.url_logout_pm)
        return


    ## PRODUCT DETAIL SECTION
        
    # Generate Pm Product Detail URL when Passed self.style ( for self.style in style_list: self.get_url_proddesc()    ) or style?not sure
    def get_url_proddesc(self):
        self.pmurl_style    = "http://pm.bluefly.corp/manager/product/productdetails.html?id={0}".format(self.style)
        return self.pmurl_style

  
    def submit_save_proddesc(self):
        pmurlpdp = self.get_url_proddesc()        
        ## Open Page
        self.open(pmurlpdp)

        ## Preprocess Response to Account for Bad HTML         
        response = self.http_response(self.request,self.response())
        headers = response.info()  
        headers["Content-type"] = "text/html; charset=utf-8"
        response.set_data(response.get_data().replace("<!---", "<!--"))
        self.set_response(response)
        
         #submit='Save')
        # Referer 
        self.addheaders = [('Referer', '{0}'.format(pmurlpdp))]
        # Content Type is form
        self.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        try:
            ## Select the main(and only) form nr=
            self.select_form(nr=0)
            self.submit()
        except mechanize._mechanize.FormNotFoundError:
            pass
            return


    def get_set_image_on_off(self):
        mainImageCheck          = self.form.controls[25]
        zoomImageCheck          = self.form.controls[27]
        alternateImage1Check    = self.form.controls[30]
        alternateImage2Check    = self.form.controls[32]
        alternateImage3Check    = self.form.controls[34]
        alternateImage4Check    = self.form.controls[36]
        alternateImage5Check    = self.form.controls[38]
        mainImageSwatchText     = self.form.controls[41]


    def get_api_endpoints(self):
        import requests
        self.hostname   =   ''
        self.apiroot    =   ''
        self.apiname    =   ''
        self.endpoint   =   ''
        self.objects    =   ''
        self.fmt        =   ''

        if not self.hostname:
            self.hostname = 'http://pm.bluefly.corp/manager/product/{0}'.format(self.apiname)
        if not self.apiroot:
            self.apiroot = 'api/mergecolorstyle.html'
        if not self.apiname:
            self.apiname = ''
        if not self.objects:
            self.objects = ''
        if not self.fmt:
            self.fmt = '?format=json'
        
        url = os.path.join(self.hostname,self.apiroot,self.apiname,endpoint,self.objects,self.fmt)
        r = requests.get(url).json()
        endpoints = r.keys()
        return endpoints, r


    ##  MERGE SECTION
    def get_url_prodmerge(self):
        self.mergeurl_style    = "http://pm.bluefly.corp/manager/product/mergecolorstyle.html?id={0}".format(self.style)
        return self.mergeurl_style


    def select_merge_colorstyle(self):
        ## Select the check box
        self.select_form(nr=0)
        self.controls
        return

    def submit_save_prodmerge(self):
        pmmergeurl = self.get_url_prodmerge()        
        ## Open Page
        self.open(pmmergeurl)
        self.Formid="mergeStylesModel" 
        self.Formname="mergeform" 
        self.Formmethod="post" 
        self.Formaction=pmmergeurl.strip('http://pm.bluefly.corp/')
        self.Inputid="mergingStyleIndex" 
        self.Inputname="mergingStyleIndex" 
        self.Inputtype="hidden" 
        self.Inputvalue=""
            
        try:
            ## Select the main(and only) form nr=
            self.select_form(nr=0)
            
            ## Select the style to merge into current style
            select_merge_checkbox = select_merge_colorstyle(self.style)

            ## Merge em
            self.submit()
        
        except mechanize._mechanize.FormNotFoundError:
            pass
            return


###########################
###########################
###########################
def main():
    import mechanize, cookielib
    import os,sys,re,glob

    #url = sys.argv[1]

    # Browser
    #br = mechanize.Browser()
    br = PMbflyMyBrowser()
    
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    #br.addheaders = [('User-agent',
    #                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    try:
        styles_list = sys.argv[1:]
    except:
        styles_list = ['336844201','336842001','336841901', '336841801','336841701', '336841601','336841501']
        pass

    ## First Login with the already supplied creds
    br.login_pm()

    # Read in style list which goes to each styles product detail page then clicks submit
    for style in styles_list:
        br.style = style
        res = br.submit_save_proddesc()
        try:
            print res.read()
        except AttributeError:
            pass
            print 'None Type Passed {}'.format(style)
        except mechanize._mechanize.FormNotFoundError:
            pass
            ## Logout Log back in on error
            br.logout_pm()
            br.login_pm()
    
    br.logout_pm()
    br.close()

if __name__ == "__main__":
    main()
