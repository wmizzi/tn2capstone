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
        
        data = json.dumps({"UserInfo":{"user id":self.client_mac,"timestamp":self.timestamp,"ip":"null","lat":0,"lon":0},
                           "SpeedTests":{"TCP":{"upload":-1,"download":-1},
                                         "UDP":{"download":{"4k":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1},
                                                            "1080p":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1},
                                                            "720p":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1},
                                                            "420p":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1}},
                                                "upload":{"screensharing":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1},
                                                          "standard_video_calling":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1},
                                                          "hd_video_calling":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1}},
                                                "2way":{"high_VOIP":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1,"latency":-1},
                                                        "low_VOIP":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1,"latency":-1},
                                                        "gaming":{"PLR":-1,"jitter_lat":-1,"jitter_iat":-1,"latency":-1}}}},
                           "TRACEROUTE":{}})
        
        jsonFile = open(self.filename, "w+")
        jsonFile.write(data)
        
        print self.filename
    
        
    def json_update_tcp(self, iperf_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["TCP"]["upload"] = iperf_results["tcp_upload"]
        data["SpeedTests"]["TCP"]["download"] = iperf_results['tcp_download']
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))

    def json_update_4k(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["download"]["4k"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["download"]["4k"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["download"]["4k"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
    
    def json_update_1080p(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["download"]["1080p"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["download"]["1080p"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["download"]["1080p"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
    
    
    def json_update_720p(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["download"]["720p"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["download"]["720p"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["download"]["720p"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
    
    def json_update_420p(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["download"]["420p"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["download"]["420p"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["download"]["420p"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        

    def json_update_screensharing(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["upload"]["screensharing"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["upload"]["screensharing"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["upload"]["screensharing"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
    def json_update_standard_video_calling(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["upload"]["standard_video_calling"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["upload"]["standard_video_calling"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["upload"]["standard_video_calling"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        

    def json_update_hd_video_calling(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["upload"]["hd_video_calling"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["upload"]["hd_video_calling"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["upload"]["hd_video_calling"]["jitter_iat"] = udp_results["jitter_iat"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
    

    def json_update_high_VOIP(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["2way"]["high_VOIP"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["2way"]["high_VOIP"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["2way"]["high_VOIP"]["jitter_iat"] = udp_results["jitter_iat"]
        data["SpeedTests"]["UDP"]["2way"]["high_VOIP"]["latency"] = udp_results["latency"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))


    def json_update_high_VOIP(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["2way"]["low_VOIP"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["2way"]["low_VOIP"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["2way"]["low_VOIP"]["jitter_iat"] = udp_results["jitter_iat"]
        data["SpeedTests"]["UDP"]["2way"]["low_VOIP"]["latency"] = udp_results["latency"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
    def json_update_gaming(self, udp_results):
        
        jsonFile = open(self.filename,"r+")
        data = json.load(jsonFile)
        
        data["SpeedTests"]["UDP"]["2way"]["gaming"]["PLR"] = udp_results["PLR"]
        data["SpeedTests"]["UDP"]["2way"]["gaming"]["jitter_lat"] = udp_results["jitter_lat"]
        data["SpeedTests"]["UDP"]["2way"]["gaming"]["jitter_iat"] = udp_results["jitter_iat"]
        data["SpeedTests"]["UDP"]["2way"]["gaming"]["latency"] = udp_results["latency"]
        
        jsonFile2 = open(self.filename, "w+")
        jsonFile2.write(json.dumps(data))
        
        

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
        
    
    