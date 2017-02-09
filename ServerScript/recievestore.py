# created by Angus Clark 9/2/17
# ToDo impliment traceroute function into this 
# Perhaps get rid of unnecessary itemediate temp file

import socket
import os
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '130.56.253.43'
#print host
port = 5201 # Change port (must enable security settigns of server)
s.bind((host,port))
s.listen(5)

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
    info["UserInfo"]["ip"] = addr[0] # store ip address of sender
        
    id = info["UserInfo"]["user id"]
    timestamp = info["UserInfo"]["timestamp"]
        
    os.system('mkdir /home/ubuntu/data/'+id)
    path = "/home/ubuntu/data/" + id + "/"
    filename = timestamp + '.json'
        
    savefile = open(path + filename, 'w+')
    savefile.write(json.dumps(info))
    savefile.close()