import json
import uuid
import datetime
import os

def json_init():
    
    client_mac = str(hex(uuid.getnode()))
    timestamp = datetime.datetime.now().strftime(" %H-%M %d-%m-%y")
    
    #filename = client_mac + timestamp + '.json'
    filename = os.path.abspath('results/' + client_mac + timestamp + '.json')
    
    data = json.dumps({"UserInfo":{"user id":client_mac,"timestamp":timestamp},
                       "IPERF":{"TCP":{"upload":-1,"download":-1},
                                "UDP":{"upload":-1,"download":-1,"packetloss":-1,"jitter":-1}},
                       "HTTP":{"GET":{"site1":-1,"site2":-1,"site3":-1,"avg":-1},
                               "POST":{"site1":-1,"site2":-1,"site3":-1,"avg":-1}},
                       "FTP":{"download":-1,"upload":-1}})
    
    jsonFile = open(filename, "w+")
    jsonFile.write(data)

    return filename
    
def json_update_iperf(filename,tcpup,tcpdown,udpup,udpdown,udploss,udpjitter):
    
    jsonFile = open(filename,"r+")
    data = json.load(jsonFile)
    
    data["IPERF"]["TCP"]["upload"] = tcpup
    data["IPERF"]["TCP"]["download"] = tcpdown
    data["IPERF"]["UDP"]["upload"] = udpup
    data["IPERF"]["UDP"]["download"] = udpdown
    data["IPERF"]["UDP"]["packetloss"] = udploss
    data["IPERF"]["UDP"]["jitter"] = udpjitter
    
    jsonFile2 = open(filename, "w+")
    jsonFile2.write(json.dumps(data))
    
    return 0
    
def json_update_http(filename,s1get,s2get,s3get,gavg,s1post,s2post,s3post,pavg):
    
    jsonFile = open(filename,"r+")
    data = json.load(jsonFile)
    
    data["HTTP"]["GET"]["site1"] = s1get
    data["HTTP"]["GET"]["site2"] = s2get
    data["HTTP"]["GET"]["site3"] = s3get
    data["HTTP"]["GET"]["avg"] = gavg
    data["HTTP"]["POST"]["site1"] = s1post
    data["HTTP"]["POST"]["site2"] = s2post
    data["HTTP"]["POST"]["site3"] = s3post
    data["HTTP"]["POST"]["avg"] = pavg
    
    jsonFile2 = open(filename, "w+")
    jsonFile2.write(json.dumps(data))
    
    return 0

def json_update_ftp(filename,down,up):
    
    jsonFile = open(filename,"r+")
    data = json.load(jsonFile)
    
    data["FTP"]["download"] = down
    data["FTP"]["upload"] = up
    
    jsonFile2 = open(filename, "w+")
    jsonFile2.write(json.dumps(data))
    
    return 0
    
    
    
    