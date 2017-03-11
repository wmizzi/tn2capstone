import socket
import time

DEBUG = 1

BUFFER = 2048
HOST = ''
PORT = 5203

ADDR = (HOST,PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind(ADDR)
    if DEBUG:
        print 'server started'
except Exception:
    time.sleep(1)
    if DEBUG:
        print 'Error binding addr'

while True:
    data, addr = sock.recvfrom(BUFFER)
    time.sleep(1)
    splitdata = data.split(',')
    
    packet_size = int(splitdata[0])
    no_of_packets = int(splitdata[1])
    packets_per_second = int(splitdata[2])
    
    IDT = 1. / packets_per_second
    
    padding = ''
    
    for j in range(78, packet_size):
        padding = padding + str(1)
    for i in range(1, no_of_packets):
        time.sleep(IDT)
        snt_time = time.time()
        sock.sendto(str((str('%08d' % i), snt_time, padding)), addr)
    