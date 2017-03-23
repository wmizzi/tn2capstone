import subprocess
import os
import json
import platform

class IperfClient:
    #This class sets variables for iperf tests as well assert
    #running an iperf test (must have iperf in local directory
    #Notes this will only run in windows
    
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.packetlength = ""
        self.conn = 1
        self.protocol = ""
        self.direction = ""
        self.directiontag = ""
        self.runtime = 10
        
        # for UDP
        self.bandwidth = ""
        
        # Results
        self.tcpup = -1
        self.tcpdown = -1
        self.udpup = -1
        self.udpdown = -1
        self.udpjitterup = -1
        self.udppacketlossup = -1
        self.udpjitterdown = -1
        self.udppacketlossdown = -1
    # Sets target ip address and port
    def setTarget(self,addr,port):
        self.addr = addr
        self.port = port
    # Sets parameters for upload (these can be hardcoded to remove variation)
    def setParams(self, bandwidth, packetlen=""):
        self.bandwidth = bandwidth
        self.packetlen = packetlen
    # Sets the number of parallel connections
    def setConnections(self,conn):
        self.conn = conn
    # Sets the iperf session to download
    def setDownload(self):
        self.direction = "-r"
        self.directiontag = "down"
    # Sets Iperf sessino to upload (default)
    def setUpload(self):
        self.direction = ""
        self.directiontag = "up"
    # Sets protocol to use (either tcp or udp)
    def setProtocol(self,protocol):
        self.protocol = protocol.lower()   
        
    def setRuntime(self,runtime):
        self.runtime = runtime   
    
    def setBandwidth(self,bandwidth):
        self.bandwidth = bandwidth
    # Runs iperf session
    def openConnection(self):
        #PLACE HOLDER
        print 'NOT YET IMPLIMENTED'
        
        
    def run(self):
        try:
            
            command = ""
            
            if platform.system() == 'Windows':
                filepath = os.path.dirname(os.path.abspath(__file__))
                command = command + filepath + '\iperf3.exe'
            else:
                command = command + 'sudo iperf3'
            command = command + ' -c ' + self.addr
            command = command + ' -p ' + str(self.port) 
            command = command + ' -t ' + str(self.runtime)
            command = command + ' -P ' + str(self.conn)
            
            if self.protocol == 'udp':
                command = command + ' -u -b ' + str(self.bandwidth)
            
            if self.directiontag == 'down':
                command = command + ' -R'
            command = command + ' -J'
            print command
            if platform.system() == 'Windows':
                proc = subprocess.Popen(command,stdout=subprocess.PIPE)
                output = proc.stdout.read()
            else:
                output = os.system(command)
          
            data = json.loads(output)
            
        except Exception:
            print 'Error - trying next port'
            while self.port < 5202:
                self.port=self.port+1
                self.run()
        
        try:
            
            if self.protocol == 'tcp' and self.directiontag == 'down':
                self.tcpdown = data["end"]["sum_received"]["bits_per_second"]
        
            if self.protocol == 'tcp' and self.directiontag == 'up':
                self.tcpup = data["end"]["sum_received"]["bits_per_second"]
            if self.protocol == 'udp' and self.directiontag == 'up':
                self.udpdown = data["end"]["sum"]["bits_per_second"]
                self.udpjitterdown = data["end"]["sum"]["jitter_ms"]
                self.udppacketlossdown = data["end"]["sum"]["lost_percent"]
            if self.protocol == 'udp' and self.directiontag == 'down':
                self.udpup = data["end"]["sum"]["bits_per_second"]
                self.udpjitterup = data["end"]["sum"]["jitter_ms"]
                self.udppacketlossup = data["end"]["sum"]["lost_percent"]
                
        except:
            print 'error running iPerf - no data found'
            #while self.port < 5202:
            #    self.port=self.port+1
            #    self.run()
        
            
    def getResults(self):
        return {'tcp_upload':self.tcpup, 'tcp_download':self.tcpdown,
                    'udp_upload':self.udpup , 'udp_upload_jitter' : self.udpjitterup , 'udp_upload_loss' : self.udppacketlossup,
                    'udp_download' : self.udpdown , 'udp_download_jitter' : self.udpjitterdown , 'udp_download_loss':self.udppacketlossdown}
    