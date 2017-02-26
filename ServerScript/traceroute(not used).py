#Created by Angus Clark 12/01/2017

import sys
import socket
import time

def traceroute(hostname):
    destination = socket.gethostbyname(hostname)
    port = 33434 # standard icmp port
    max_hops = 30
    print "target %s" %hostname
    print "targer ip: %s" %destination
    
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    
    while True:
        recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        sendsock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recvsock.bind(("",port))
        sendsock.sento("",(hostname,port))
        currentaddr = None
        currenthostname = None
        
        try:
            data, currentaddr = recvsock.recvfrom(512)
            recv_time = time.time()
            currentaddr = currentaddr[0]
            
            try:
                currenthostname = socket.gethostbyaddr(currentaddr)[0]
            except:
                currenthostname = currentaddr
        except socket.error:
            pass
        
        finally:
            sendsock.close()
            recvsock.close()
            
        if currentaddr is not None:
            currenthost = "%s : %s" %(currenthostname,currentaddr)
        else:
            currenthost = "*"
            
        print "%d: %s" % (ttl,currenthost)
        print 1000*(recv_time - send_time)
        
        ttl +=1
        
        if currentaddr == destination or ttl> max_hops:
            break
    
if __name__ == "__main__":
    traceroute(sys.arg[1])
    