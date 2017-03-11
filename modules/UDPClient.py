import sys
import json
import time
import socket
import numpy

class UDPClient:
    
    def __init__(self, addr):
        
        self.addr = addr
        self.port = -1 # Change on port allocation finalisation
    
        self.packet_size = -1
        self.no_of_packets = -1
        self.packets_per_sec = -1
        
        # Download results
        
        self.PLR_dwn = -1
        self.std_dwn_lat = -1
        self.std_dwn_IAT =  -1
        self.mean_dwn_IAT =  -1
        self.tot_dwn_time = -1
        
        # Upload results
        
        self.PLR_up = -1
        self.std_up_lat = -1
        self.std_up_IAT = -1
        self.mean_up_IAT = -1
        self.tot_up_time = -1
        
    def UDP_Reflector(self, port, packet_size, no_of_packets, packets_per_sec):
        self.port = port
        self.packet_size = packet_size
        self.no_of_packets = no_of_packets
        self.packets_per_sec = packets_per_sec
        
    def UDP_Download(self, port, packet_size, no_of_packets, packets_per_sec):
        self.port = port
        self.packet_size = packet_size
        self.no_of_packets = no_of_packets
        self.packets_per_sec = packets_per_sec
        
        dwn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        command = str(self.packet_size) + ',' + str(self.no_of_packets) + ',' + str(self.packets_per_sec) + ',' + str(('%.5f' % time.time()))
        dwn_sock.sendto(command, (self.addr,self.port)) # send command with packets to be generated and sent back
        dwn_sock.settimeout(2) # No packet received in 2 seconds will end service
        
        BUFFER = 2048
        latency = []
        rcvd_time = []
        #starttime = time.time()
        packets_rcvd = 0
        while True: #starttime + no_of_packets/packets_per_sec + 5 - time.time() > 0:
            try:
                data, addr = dwn_sock.recvfrom(BUFFER)
            except Exception:
                break
            time_rcvd = time.time()
            latency.append(float((data.split(',')[1])) - time_rcvd)
            rcvd_time.append(time_rcvd)
            packets_rcvd = packets_rcvd + 1
            
        
        dwn_sock.close()
        
        lat = numpy.asarray(latency)
        RCV = numpy.asarray(rcvd_time)
        IAT = numpy.diff(RCV)
        
        self.tot_dwn_time = rcvd_time[packets_rcvd-1] - rcvd_time[1]
        self.dwn_data_transfer = packets_rcvd * packet_size # in bytes
        self.PLR_dwn = 1 - float(packets_rcvd) / no_of_packets
        self.mean_dwn_lat =  numpy.mean(lat) # irrelevant because unsyncs clocks
        self.std_dwn_lat = numpy.std(lat)
        self.std_dwn_IAT =  numpy.std(IAT)
        self.mean_dwn_IAT =  numpy.mean(IAT)
        
        
    def UDP_Upload(self, port, handler_port, packet_size, no_of_packets, packets_per_sec):
        self.port = port
        self.packet_size = packet_size
        self.no_of_packets = no_of_packets
        self.packets_per_sec = packets_per_sec
        
        BUFFER = 2048
        
        upload_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        up_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        handler_addr = (self.addr , handler_port)
        upload_addr = (self.addr , self.port)
        
        upload_handler.connect(handler_addr)
        
        command = str(packet_size) + ',' + str(no_of_packets) + ',' + str(packets_per_sec)
        
        upload_handler.send(command)
        
        #time.sleep(1) # wait for server
        
        IDT = 1. / packets_per_sec
        packet_count_snd = 0
        
        padding = ''
        
        for j in range(78, packet_size):
            padding = padding + str(1) # pads packet to make it required size

        for i in range(1, no_of_packets +1):
            time.sleep(IDT)
            command = str(i) + ',' + str(time.time()) + ',' + padding
            up_sock.sendto(command,upload_addr)
            #up_sock.sendto(str((str('%08d' % i),"%.5f" % time.time(), padding)), upload_addr)
            packet_count_snd = packet_count_snd + 1
        
        
        test_data = upload_handler.recv(BUFFER)
        
        upload_handler.close()
        up_sock.close()
        
        results = test_data.split(',')
        
        self.PLR_up = 1 - float(results[0]) / no_of_packets
        self.std_up_lat = results[3]
        self.std_up_IAT = results[4]
        self.mean_up_IAT = results[5]
        self.tot_up_time = results[1]
        
        
        
        
        