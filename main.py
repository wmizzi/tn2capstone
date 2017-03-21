from modules import IperfClient
from lib import jsonprocesser
from modules import UDPClient
from threading import Thread
import time

#from pingClient import pingClient

'''
PORT ALLOCATIONS
***************

IPERF : 5201, 5202
UDP_DOWNLOAD : 5203
UDP_UPLOAD : 5204(handler), 5205(uploader)
UDP_REFLECTOR : 5209
FILEHANDLER : 5208

Transfer Specifications
*****************

4k stream (40Mbps 30fps)
    Packet size 1392 bytes(from youtube)
    Packets per second 3592 
    
1080p stream (8Mbps 30fps)
    Packet size 1392 bytes
    Packets per second 718
    
720p stream (5Mbps 30fps)
    Packet size 1392
    Packets per second 445
    
420p stream (2.5Mbps 30fps)
    Packet size 1392
    Packets per second 225
    
Screensharing
    Bursty bit rate (3-4 Mbps spikes with 0.07Mbps other times)
    Short 2 second spike at 4Mbps
    Packet size 800 bytes
    Packets 625 packets per second
    1250 packets

Standard_video_calling
    Bursty upload data (500kbps)
    Mean packet size 800 bytes
    Uniform dist of burst length [2,4]
    backoff probability time profile : [0,3./9,1./9,1./9,2./9,2./9,1./9]
    mean backoff = 0.0384s
    
    
    
hd_video_calling
    Bursty upload data (1.5Mbps)
    Mean packet size 1162 bytes
    Uniform dist of burst length
    backoff = 1.5Mkbps/packet_size*8*mean_burst_length
    
high quality VOIP
    Constant bitrate??
    
    



'''

upload_file = jsonprocesser.jsonprocesser()
iperf_test = IperfClient.IperfClient('130.56.253.43',5201)
udp_test = UDPClient.UDPClient('130.56.253.43')


# 4k test
#esult = udp_test.UDP_Download(5203, 1392, 10000, 3592)
#upload_file.json_update_4k(result)
#time.sleep(2)

 #1080p test
#result = udp_test.UDP_Bursty_Download(5206, 1000, 10000, 0.01257, 11)
#print result

result = udp_test.UDP_Bursty_Reflector(5209, 1000, 1000, 63, 7, 0.1)
print result
##upload_file.json_update_1080p(result)
#time.sleep(2)

#result = udp_test.UDP_Download_CBR(5203, 1000, 10000 , 875)
#print result

# 720p test
#result = udp_test.UDP_Download(5203, 1392, 10000, 445)
#upload_file.json_update_720p(result)
#time.sleep(2)

# 420p test
#result = udp_test.UDP_Download(5203, 1392, 10000, 225)
#upload_file.json_update_420p(result)
#time.sleep(2)

#time_profile = [0,3./9,1./9,1./9,2./9,2./9,1./9]
#result = udp_test.UDP_Skype_Upload_Burst(5205, 5204, 800, 1000, 1, 5, time_profile)
#print result
#print result
#down = udp_test.UDP_Download(5203, 300, 20, 1000)
#print down

#result = udp_test.UDP_Reflector(5209, 500, 1000, 500)
#print result

#upload_file.json_update_gaming(result)

#upload_file.print_json()



# Download TCP test
#iperf_test.setDownload()
#iperf_test.setProtocol('tcp')
#iperf_test.run()

# Download UDP test
#iperf_test.setProtocol('udp')
#iperf_test.run()

# Upload UDP test
#iperf_test.setUpload()
#iperf_test.run()

# Upload TCP test
#iperf_test.setProtocol('tcp')
#iperf_test.run()

#iperf_results = iperf_test.getResults()
#print iperf_results
#upload_file.json_update_iperf(iperf_results)
#upload_file.json_upload('130.56.253.43',5208)


