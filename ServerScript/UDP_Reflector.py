import socket
import time
import sys

REFLECTOR_HOST = '' # Responds to any incoming IP
REFLECTOR_PORT = 5203 # Change when port designations are finalised
BUFFER = 4096

ADDR = (REFLECTOR_HOST, REFLECTOR_PORT)

EchoServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    EchoServer.bind(ADDR)
    print "Server Started Successfully"
except Exception:
    print "ERROR **** Server Failed ***** Closing Down"
    time.sleep(5)
    sys.exit()
    
while True:
    data, client_addr = EchoServer.recvfrom(BUFFER)
    print 'Data Received'
    EchoServer.sendto('%s' % (data), addr)
    print 'Data Reflected    '

