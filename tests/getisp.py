#import html2text
import re
import sys
import urllib2

def get_ip(host):
    trac = "http://www.ip-adress.com/ip_tracer/"
    pat  = "ISP of this IP \[\?\]:\n\n([a-zA-Z ]+)"
    hdr  = {'User-Agent': 'Mozilla/5.0'} # ip-adress.com only accepts popular agents
    req  = urllib2.Request(trac + host, headers=hdr)
    page = urllib2.urlopen(req).read()

    print page

    try:
        print "ISP for %s:\n" % host, re.search(pat, text).group(1)
    except:
        print "Could not find ISP for", host

def main():
    
    get_ip('130.56.253.43')

if __name__ == "__main__":
    main()