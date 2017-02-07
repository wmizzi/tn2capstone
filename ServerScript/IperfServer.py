import os

class IperfServer:
    def __init__(self,min_port,max_port):
        self.min_port = min_port
        self.max_port = max_port
    def start_session(self):
        for port in range(self.min_port,self.max_port):
            command = 'iperf3 -s -p ' + str(port) + ' -D'
            os.system(command)