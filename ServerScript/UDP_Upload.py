import socket
import numpy
import time


BUFFER = 2048

handler_port = 5209
upload_port = 5206
incoming_host = '' # accept all clients
DEBUG = 1 # Switch to turn on and off debug mode

while True:
    
    handler_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #handler socket
    upload_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #testing socket
    handler_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    upload_socket.settimeout(2) # 2 second timeout on testing socket
    
    upload_addr = (incoming_host,upload_port)
    handler_addr = (incoming_host, handler_port)
    
    while True:
        try:
            handler_socket.bind(handler_addr)
            upload_socket.bind(upload_addr)
            if DEBUG:
                print 'sockets binded'
            break
        except Exception:
            if DEBUG:
                print 'Unable to bind sockets'
            time.sleep(5)
    
    handler_socket.listen(5)
    if DEBUG:
        print 'listening for incoming connections...'
    
    conn, addr = handler_socket.accept()
    
    if DEBUG:
        print 'Test initiated from:'
        print addr

    while True:
        try:
            test_params = conn.recv(BUFFER)
            break
        except Exception:
            if DEBUG:
                print 'Failed to receieve data'
            time.sleep(2)
            
    params = test_params.split(',')
    
    latency = []
    timing = []
    packets_rcvd = 0
    
    while True:
        try:
            data, addr = upload_socket.recvfrom(BUFFER)
        except Exception:
            break
        time_rcvd = time.time()
        latency.append(float((data.split(',')[1])) - time_rcvd)
        timing.append(time_rcvd)
        packets_rcvd = packets_rcvd + 1
        
    upload_socket.close()
    
    lat = numpy.asarray(latency)
    RCV = numpy.asarray(timing)
    IAT = numpy.diff(RCV)
    
    tot_up_time = timing[packets_rcvd -1] - timing[1]
    mean_up_lat = numpy.mean(lat) # not useful due to clock desync
    std_up_lat = numpy.std(lat)
    std_up_IAT = numpy.std(IAT)
    mean_up_IAT = numpy.mean(IAT)
    
    command = str(packets_rcvd) + ',' + str(tot_up_time) + ',' + str(mean_up_IAT) + ',' 
    command = command + str(std_up_lat) + ',' + str(std_up_IAT) + ',' + str(mean_up_IAT)
    
    conn.send(command)
    handler_socket.close()
    
    