# The Iperf Client should first run a TCP test and then a UDP test and report back 
# upload and download for both TCP and UDP as well as jtter and packet loss for UDP

# Iperf must be installed or be in local dir
import os
import platform
import time

JSON_FILE_TCP_UPLOAD = 'iperftcpu.json'
JSON_FILE_TCP_DOWNLOAD = 'iperftcpd.json'
JSON_FILE_UDP_UPLOAD = 'iperfudpu.json'
JSON_FILE_UDP_DOWNLOAD = 'iperfudpd.json'

status = 0;

windows = False # Checks if windows machine later in code

def iperfclient(ip_addr,port ,json ,debug = False):
    
    try:
        if platform.system() == 'Windows':
            windows = True
            if debug:
                print 'detected windows machine'
        # Begin TCP upload test
        if windows:
            command = 'iperf3.exe -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -J >>' + JSON_FILE_TCP_UPLOAD
        else:
            command = 'iperf3 -c ' + ip_addr + ' -p ' + str(port) +' -t 10 -J >>' + JSON_FILE_TCP_UPLOAD
            
        if debug:
            print 'Initiating tcp upload with tags: ' + command
            
        os.system(command)
        # Wait for TCP to finish (may not be necessary)    
        time.sleep(11)
        
        if windows:
            command = 'iperf3.exe -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -f M -r -J >>' + JSON_FILE_TCP_DOWNLOAD
        else:
            command = 'iperf3 -c ' + ip_addr + ' -p ' + str(port) +' -t 10 -f M -r -J >>' + JSON_FILE_TCP_DOWNLOAD
            
        if debug:
            print 'Initiating tcp download with tags: ' + command
        os.system(command)
        
        time.sleep(11)
        
       
        # Begin UDP test
        if windows:
            command = 'iperf3.exe -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -u -J >>' + JSON_FILE_UDP_UPLOAD
        else:
            command = 'iperf3 -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -u -J >>' + JSON_FILE_UDP_UPLOAD
        if debug:
            print 'Initiating udp upload with tags: ' + command    
        os.system(command)
        
        time.sleep(11)
        
        if windows:
            command = 'iperf3.exe -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -u -r -J >>' + JSON_FILE_UDP_UPLOAD
        else:
            command = 'iperf3 -c ' + ip_addr + ' -p ' + str(port) + ' -t 10 -u -r -J >>' + JSON_FILE_UDP_UPLOAD
            
        if debug:
            print 'Initiating udp download with tags: ' + command 
            
        os.system(command)
    except:
        status = 1;