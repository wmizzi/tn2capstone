import json
import urllib2
import socket
import time

class HttpClient:
    def __init__(self):
        self.hostname = 'www.youtube.com'
    def run_custom_url(self,hostname):
        dns_start = time.time()
        ip_address = socket.gethostbyname(hostname)
        dns_end = time.time()
        
        url = 'https://%s/' % hostname
        print url
        req = urllib2.Request(url)
        req.add_header('Host', hostname)

        handshake_start = time.time()
        stream = urllib2.urlopen(req)
        handshake_end = time.time()

        data_start = time.time()
        data_length = len(stream.read())
        data_end = time.time()

        #print 'DNS time            = %.2f ms' % ((dns_end - dns_start) * 1000)
        #print 'HTTP handshake time = %.2f ms' % ((handshake_end - handshake_start) * 1000)
        #print 'HTTP data time      = %.2f ms' % ((data_end - data_start) * 1000)
        #print 'Data received       = %d bytes' % data_length
        #print 'HTTP data rate      = %.2f bytes/second' % (float(data_length) / float(data_end - data_start))
        
        return {"DNS" : ((dns_end - dns_start) * 1000) , "HTTP Handshake" : ((handshake_end - handshake_start) * 1000), "DATA_RATE" : (float(data_length) / float(data_end - data_start))} 