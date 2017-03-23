import sys
import json
import time
import socket
import numpy
from threading import Thread

class UDPClient:
    
    def __init__(self, addr, number_of_reflects = 2):
        
        self.addr = addr
        self.port = -1 # Change on port allocation finalisation
        
        self.reflects = number_of_reflects 
        self.reflect_counter = 0
    
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
        
        # two way test
        
        self.PLR_2way = -1
        self.std_2way_lat = -1
        self.std_2way_IAT = -1
        self.mean_2way_lat = -1
        self.mean_2way_IAT = -1
        self.packets_sent_2way = 0
        self.packets_rcvd_2way = 0
        
        self.two_way_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.two_way_socket.settimeout(0.5)
        
    def two_way_send(self, port, packet_size, no_of_packets, packets_per_sec):
        IDT = 1.0 / packets_per_sec
        self.packets_sent_2way = 0
        addr = (self.addr, port)
        
        padding = ''
        message = ''
        IDT = 1.0 / packets_per_sec
        
        for j in range(45,packet_size):
            padding = padding + str(1)
        for i in range(1,no_of_packets + 1):
            time.sleep(IDT)
            sendtime = str('%.3f' % time.time())
            message = str('%08d' % i) + ',' + sendtime + ',' + padding
            self.two_way_socket.sendto(message, addr)
        time.sleep(2)
    
    def two_way_recieve(self):
        receive_ip = ''
        receive_port = 54321 # check if this needs to be specified
        addr = (receive_ip, receive_port)
        BUFFER = 2048
        try:
            self.two_way_socket.bind(addr)
        except Exception:
            print 'error : port already bound'
        
        latency = []
        rcvd_time = []
        packets_rcvd = 0
        
        while True:
            try:
                data, addr = self.two_way_socket.recvfrom(BUFFER)
            except Exception:
                break
            splitdata = data.split(',')
            time_rcvd = time.time()
            latency.append(time_rcvd - float(splitdata[1]))
            rcvd_time.append(time_rcvd)
            packets_rcvd = packets_rcvd + 1
            
        lat = numpy.asarray(latency)
        RCV = numpy.asarray(rcvd_time)
        IAT = numpy.diff(RCV)
        
        #print packets_rcvd
            
        self.mean_2way_lat = numpy.mean(lat)    
        self.std_2way_lat = numpy.std(lat)
        self.std_2way_IAT = numpy.std(IAT)
        self.packets_rcvd_2way = packets_rcvd
        
        
    def UDP_Reflector(self, port, packet_size, no_of_packets, packets_per_sec):
        
        self.two_way_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.two_way_socket.settimeout(0.5)
        
        self.port = port
        self.packet_size = packet_size
        self.no_of_packets = no_of_packets
        self.packets_per_sec = packets_per_sec
        self.reflect_counter = self.reflect_counter + 1
        
        BUFFER = 2048
        RECIEVE_IP = ''
        receiver_thread = Thread(target=self.two_way_recieve)
        receiver_thread.daemon = True
        receiver_thread.start()
        time.sleep(.2)
        send_thread = Thread(target = self.two_way_send, args = (port, packet_size, no_of_packets, packets_per_sec)).start()
        
        time.sleep(5 + 2 * no_of_packets / packets_per_sec)
     
        self.two_way_socket.close()
        
        return {"PLR" : 1. - float(self.packets_rcvd_2way) / no_of_packets, "jitter_lat" : self.std_2way_lat, "jitter_iat" : self.std_2way_IAT, "latency" : self.mean_2way_lat} 
               
    def UDP_Download_CBR(self, port, packet_size, no_of_packets, packets_per_sec):
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
        recieved_data = []
        #starttime = time.time()
        packets_rcvd = 0
        while True: #starttime + no_of_packets/packets_per_sec + 5 - time.time() > 0:
            try:
                data, addr = dwn_sock.recvfrom(BUFFER)
            except Exception:
                break
            time_rcvd = time.time()
            latency.append(time_rcvd - float((data.split(',')[1])))
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
        
        return {"PLR" : self.PLR_dwn , "jitter_lat" : self.std_dwn_lat , "jitter_iat" : self.std_dwn_IAT}
        
        
    def UDP_Upload_CBR(self, port, handler_port, packet_size, no_of_packets, packets_per_sec):
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
        
        return {"PLR" : self.PLR_up , "jitter_lat" : self.std_up_lat , "jitter_iat" : self.std_up_IAT}
        
        
    def UDP_Bursty_Upload_Uniform(self, port, handler_port, packet_size, no_of_packets, burst_length_lower, burst_length_upper, backoff_lower, backoff_upper):
        
        BUFFER = 2048
        
        upload_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        up_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        handler_addr = (self.addr , handler_port)
        upload_addr = (self.addr , port)
        
        upload_handler.connect(handler_addr)
        
        command = str(packet_size) + ',' + str(no_of_packets)
        
        upload_handler.send(command)
        
        packet_count_snd = 0
        
        padding = ''
        
        for j in range(78, packet_size):
            padding = padding + str(1) # pads packet to make it required size

        while packet_count_snd < no_of_packets:
            #backoff = numpy.argmax(numpy.random.multinomial(1,time_profile))/100.0
            backoff = numpy.random.uniform(backoff_lower,backoff_upper)/100.0
            burst_length = numpy.random.uniform(burst_length_lower,burst_length_upper)
            #burst_length = numpy.argmax(numpy.random.multinomial(1,[306./11977,186./11977,310./11977,181./11977,171./11977,2306./11977,3131./11977,2147./11977,1482./11977,1665./11977,92./11977]))
            burst = 0
            #print backoff
            while burst < burst_length and packet_count_snd < no_of_packets:
                #time.sleep(0.001)
                command = str(packet_count_snd) + ',' + str(time.time()) + ',' + padding
                up_sock.sendto(command,upload_addr)
                packet_count_snd = packet_count_snd + 1
                #print packet_count_snd
                burst = burst + 1
            time.sleep(backoff)
        
        
        test_data = upload_handler.recv(BUFFER)
        
        upload_handler.close()
        up_sock.close()
        
        results = test_data.split(',')
        
        self.PLR_up = 1 - float(results[0]) / no_of_packets
        self.std_up_lat = results[3]
        self.std_up_IAT = results[4]
        self.mean_up_IAT = results[5]
        self.tot_up_time = results[1]
        
        return {"PLR" : self.PLR_up , "jitter_lat" : self.std_up_lat , "jitter_iat" : self.std_up_IAT}
    
    def UDP_Bursty_Upload(self, port, handler_port, packet_size, no_of_packets, burst_length_lower, burst_length_upper, time_profile):
        
        BUFFER = 2048
        
        upload_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        up_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        handler_addr = (self.addr , handler_port)
        upload_addr = (self.addr , port)
        
        upload_handler.connect(handler_addr)
        
        command = str(packet_size) + ',' + str(no_of_packets)
        
        upload_handler.send(command)
        
        packet_count_snd = 0
        
        padding = ''
        
        for j in range(78, packet_size):
            padding = padding + str(1) # pads packet to make it required size

        while packet_count_snd < no_of_packets:
            backoff = numpy.argmax(numpy.random.multinomial(1,time_profile))/100.0
            burst_length = numpy.random.uniform(burst_length_lower,burst_length_upper)
            #burst_length = numpy.argmax(numpy.random.multinomial(1,[306./11977,186./11977,310./11977,181./11977,171./11977,2306./11977,3131./11977,2147./11977,1482./11977,1665./11977,92./11977]))
            burst = 0
            #print backoff
            while burst < burst_length and packet_count_snd < no_of_packets:
                #time.sleep(0.001)
                command = str(packet_count_snd) + ',' + str(time.time()) + ',' + padding
                up_sock.sendto(command,upload_addr)
                packet_count_snd = packet_count_snd + 1
                #print packet_count_snd
                burst = burst + 1
            time.sleep(backoff)
        
        
        test_data = upload_handler.recv(BUFFER)
        
        upload_handler.close()
        up_sock.close()
        
        results = test_data.split(',')
        
        self.PLR_up = 1 - float(results[0]) / no_of_packets
        self.std_up_lat = results[3]
        self.std_up_IAT = results[4]
        self.mean_up_IAT = results[5]
        self.tot_up_time = results[1]
        
        return {"PLR" : self.PLR_up , "jitter_lat" : self.std_up_lat , "jitter_iat" : self.std_up_IAT}
        
    def UDP_Bursty_Download(self, port, packet_size, no_of_packets, backoff, burst_length):
            self.port = port
            self.packet_size = packet_size
            self.no_of_packets = no_of_packets
            
            dwn_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            command = str(self.packet_size) + ',' + str(self.no_of_packets) + ',' + str(backoff) + ',' + str(burst_length)
            dwn_sock.sendto(command, (self.addr,port)) # send command with packets to be generated and sent back
            dwn_sock.settimeout(2) # No packet received in 2 seconds will end service
            
            BUFFER = 2048
            latency = []
            rcvd_time = []
            #starttime = time.time()
            packets_rcvd = 0
            while True: 
                try:
                    data, addr = dwn_sock.recvfrom(BUFFER)
                    #print 'rec'
                except Exception:
                    #print 'timeout'
                    break
                time_rcvd = time.time()
                latency.append(time_rcvd - float((data.split(',')[1])))
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
            
            return {"PLR" : self.PLR_dwn , "jitter_lat" : self.std_dwn_lat , "jitter_iat" : self.std_dwn_IAT}
    def two_way_bursty_send(self, port, packet_size, no_of_packets, burst_length, backoff):
        
        self.packets_sent_2way = 0
        addr = (self.addr, port)
        
        padding = ''
        message = ''
     
        for j in range(78,packet_size):
            padding = padding + str(1)
            
        while self.packets_sent_2way < no_of_packets:
            time.sleep(backoff)
            burst = 0
            while burst<burst_length and self.packets_sent_2way < no_of_packets:
                 sendtime = str('%.3f' % time.time())
                 message = str(self.packets_sent_2way) + ',' + sendtime + ',' + padding
                 self.two_way_socket.sendto(message, addr)
                 burst = burst + 1
                 self.packets_sent_2way = self.packets_sent_2way + 1
        print 'finished sending'
        time.sleep(2)

    def UDP_Bursty_Reflector(self, port, packet_size, no_of_packets, packets_per_sec, burst_length, backoff):
            
            self.port = port
            self.packet_size = packet_size
            self.no_of_packets = no_of_packets
            self.packets_per_sec = packets_per_sec
          
            
            BUFFER = 2048
            RECIEVE_IP = ''
            receiver_thread = Thread(target=self.two_way_recieve)
            receiver_thread.daemon = True
            receiver_thread.start()
            time.sleep(.2)
            send_thread = Thread(target = self.two_way_bursty_send, args = (port, packet_size, no_of_packets, burst_length, backoff)).start()
            
            time.sleep(5 + 2 * no_of_packets / packets_per_sec)
            self.two_way_socket.close()
            
            return {"PLR" : 1. - float(self.packets_rcvd_2way) / no_of_packets, "jitter_lat" : self.std_2way_lat, "jitter_iat" : self.std_2way_IAT, "latency" : self.mean_2way_lat} 