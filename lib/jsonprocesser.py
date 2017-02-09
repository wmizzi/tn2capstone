import json
import uuid
import datetime
import os
import socket

class jsonprocesser:
    

    def __init__(self):
        
        self.client_mac = str(hex(uuid.getnode()))
        self.timestamp = datetime.datetime.now().strftime("%H-%M_%d-%m-%y")
        
        #filename = client_mac + timestamp + '.json'
        self.filename = os.path.abspath('results/' + self.client_mac + self.timestamp + '.json')
        
        data = json.dumps({"UserInfo":{"user id":self.client_mac,"timestamp":self.timestamp,"ip":"null"},
                           "IPERF":{"TCP":{"upload":-1,"download":-1},"UDP":{"upload":-1,"download":-1,"packetloss":-1,"jitter":-1}},
                           "HTTP":{"GET":{"site1":-1,"site2":-1,"site3":-1,"avg":-1},"POST":{"site1":-1,"site2":-1,"site3":-1,"avg":-1}},
                           "TRACEROUTE":{}})
        
        jsonFile = open(self.filename, "w+")
        jsonFile.write(data)
        
        print self.filename
    
        
    def json_update_iperf(self, iperf_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["IPERF"]["TCP"]["upload"] = iperf_results["tcp_upload"]
        data["IPERF"]["TCP"]["download"] = iperf_results['tcp_download']
        data["IPERF"]["UDP"]["upload"] = iperf_results['udp_upload']
        data["IPERF"]["UDP"]["download"] = iperf_results['udp_download']
        data["IPERF"]["UDP"]["packetloss"] = iperf_results['udp_download_loss']
        data["IPERF"]["UDP"]["jitter"] = iperf_results['udp_download_jitter']
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
        return 0
        
    def json_update_http(self,s1get,s2get,s3get,gavg,s1post,s2post,s3post,pavg):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["HTTP"]["GET"]["site1"] = s1get
        data["HTTP"]["GET"]["site2"] = s2get
        data["HTTP"]["GET"]["site3"] = s3get
        data["HTTP"]["GET"]["avg"] = gavg
        data["HTTP"]["POST"]["site1"] = s1post
        data["HTTP"]["POST"]["site2"] = s2post
        data["HTTP"]["POST"]["site3"] = s3post
        data["HTTP"]["POST"]["avg"] = pavg
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
        return 0
    
    def json_update_ftp(self,down,up):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["FTP"]["download"] = down
        data["FTP"]["upload"] = up
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
        return 0
        
    def json_upload(self,server_ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f = open(self.filename,'rb')
        
        l = f.read(1024)
        print l
        
        s.connect((server_ip,port))
        
        while(l):
            s.send(l)
            l= f.read(1024)
        f.close()
        #s.shutdown(socket.SHUT_WR)
        s.close
        
    def print_json(self):
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        print data
        
    
    