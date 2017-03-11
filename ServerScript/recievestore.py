# created by Angus Clark 9/2/17 updated 27/2/17
# ToDo impliment traceroute function into this 
# Perhaps get rid of unnecessary itemediate temp file

import socket
import os
import json
import my_traceroute

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '130.56.253.43'
#print host
port = 5201 # Change port (must enable security settigns of server)
s.bind((host,port))
s.listen(5)
MAX_HOPS = 30 # max hops for traceroute

while True:
    c, addr = s.accept() #accept incoming Connection
    f = open('temp.json','wb') # open blank binary to dump incoming data
    #print addr[0]
    l = c.recv(1024)
    while(l):
        # Dump data into temp file and get next chunk of data
        f.write(l)
        l = c.recv(1024)
    f.close()
    c.close()
        
    tempfile = open('temp.json','rb')
    info = json.load(tempfile)
    info["UserInfo"]["ip"] = addr[0] # store ip address of sendercd
    
    last_addr = '0.0.0.0' # placeholder for first iteration
    for hop in range(1,MAX_HOPS):
        result = my_traceroute.traceroute(hop, info["UserInfo"]["ip"])
        #print result
        if result == -1:
            break
        if result[1] == last_addr:
            break
        info["TRACEROUTE"][str(result[0])] = {}
        info["TRACEROUTE"][str(result[0])].update({'node':result[1], 'rtt':result[2]})
        last_addr = result[1]
        
        
    id = info["UserInfo"]["user id"]
    timestamp = info["UserInfo"]["timestamp"]
        
    os.system('mkdir /home/ubuntu/data/'+id)
    path = "/home/ubuntu/data/" + id + "/"
    filename = timestamp + '.json'
        
    savefile = open(path + filename, 'w+')
    savefile.write(json.dumps(info))
    savefile.close()