import socket
import time
import sys
from threading import Thread

# inputs

DEST_IP = '130.56.253.43'
UDP_DEST_PORT = 5203 # Change later for security
PACKET_SIZE = 2,00 # Datagram size in bytes
NO_OF_PACKETS = 1000 # Number of packets to send
PACKETS_PER_SEC = 800 # Packets to be sent per second

RECIEVE_IP = ''
RECIEVE_PRT = 54321 # Port for incoming packets
BUFFER = 4096
global sock

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_recieve(RECIEVE_IP, RECIEVE_PRT):
    ADDR = (RECIEVE_IP, RECIEVE_PRT)
    #rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    global packets_rcvd
    global cum_delay
    packets_rcvd = 0
    cum_delay = 0.0
    
    try:
        sock.bind(ADDR)
        print 'Server listening on', ADDR
    except Exception:
        print 'ERROR - binding failed'
    
    while True:
        data, addr = sock.recvfrom(BUFFER)
        splitdata = data.split(',')
        timecount = splitdata[0].strip("('")
        rt_delay = (time.time() - float(timecount))
        packet_number = str(splitdata[1].strip("' '"))
        packet_number = packet_number.lstrip('0')
        
        # Write to file
        outfile = open('udp_testresults.csv',"a").write(str(time.ctime()+','+'received , '+ packet_number+' , '+str(rt_delay)+'\n'))
        print (time.ctime()+','+'received , '+ packet_number+' , '+str(rt_delay))
        packets_rcvd = packets_rcvd + 1
        cum_delay = cum_delay + rt_delay
        
def udp_send(DEST_IP, UDP_DEST_PORT, PACKET_SIZE, NO_OF_PACKETS,PACKETS_PER_SEC):
    IDT = 1./PACKETS_PER_SEC #Inter departure time
    packet_count_snd = 0
    
    print "Client Started!"
    print "target IP:",DEST_IP
    print "target port",UDP_DEST_PORT
    print "Packets to send", NO_OF_PACKETS
    print "MegaBytes to send/second", PACKETS_PER_SEC*PACKET_SIZE/1000000.0
    
    padding = ''
    
    for j in range(78,PACKET_SIZE):
        padding = padding + str(1)
        
    for i in range(1,NO_OF_PACKETS+1):
        time.sleep(IDT)
        #send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str(("%.5f" % time.time(),str('%08d' % i), padding)), (DEST_IP, UDP_DEST_PORT) )
        packet_count_snd = packet_count_snd+1
        
    time.sleep(5) # wait for packets to be recieved
    print packet_count_snd
    print packets_rcvd
    
if __name__ == '__main__':
    receiver_thread = Thread(target=udp_recieve, args=(RECIEVE_IP, RECIEVE_PRT))
    receiver_thread.daemon=True
    receiver_thread.start()
    time.sleep(1)
    sender_thread = Thread(target=udp_send, args=(DEST_IP, UDP_DEST_PORT, PACKET_SIZE, NO_OF_PACKETS, PACKETS_PER_SEC)).start()
    
    
