from modules import IperfClient
from lib import jsonprocesser
from modules import UDPClient
from threading import Thread
import time

#from pingClient import pingClient

'''

***** NOTES ****

Add initial setup including simple ping, DNS etc (maybe so popular website response times)

PORT ALLOCATIONS
***************

IPERF : 5201, 5202
UDP_DOWNLOAD : 5203, 5206(Bursty)
UDP_UPLOAD : 5204(handler), 5205(uploader)
UDP_REFLECTOR : 5209
FILEHANDLER : 5208

Transfer Specifications
*****************

4k stream (40Mbps 30fps)
    Packet size 1392 bytes(from youtube)
    Packets per second 3592
    Burst length = 10
    Backoff = 0.00278
    
1080p stream (8Mbps 30fps)
    Packet size 1392 bytes
    Packets per second 718
    Burst length = 8
    backoff = 0.011136
    
720p stream (5Mbps 30fps)
    Packet size 1392
    Packets per second 445
    Burst length = 6
    backoff = 0.0133
    
420p stream (2.5Mbps 30fps)
    Packet size 1392
    Packets per second 225
    Burst Length = 3
    Backoff = 0.0133
    
Screensharing
    Bursty bit rate (3-4 Mbps spikes with 0.07Mbps other times)
    Short 2 second spike at 4Mbps
    Packet size 800 bytes
    Packets 625 packets per second
    1250 packets

Standard_video_calling
    Bursty upload data (480kbps)
    Mean packet size 800 bytes
    Uniform dist of burst length [0,5]
    backoff probability time profile : [0,3./9,1./9,1./9,2./9,2./9,1./9]
    mean backoff = 0.0255
    uniform [0.01 0.07]
    mean backoff = 0.04s
    
hd_video_calling
    Bursty upload data (1.5Mbps)
    Mean packet size 1162 bytes
    Uniform dist of burst length [3,9]
    backoff = 1.5Mkbps/packet_size*8*mean_burst_length = 0.037
    backoff uniform [0.01 0.07]
    
high quality VOIP (G.711)

    Constant bitrate
    Packet size (not including header) = 160 bytes
    BR = 64 kbps
    Packets/second = 50
    
    
Low quality VoIP (G.726)

    Constant Bitrate
    Packet size (not including header) = 80 Bytes
    BR = 32 kbps
    Packets/second = 50

Online Gaming (NEED TO TEST THIS STILL) ~ 192 Kbps
    Variable Bit Rate
    Packet size = 400 bytes
    Burst length = [0,5]
    Backoff = [0, 0.1]
    
    



'''
# Initiate Upload Objects

upload_file = jsonprocesser.jsonprocesser()
iperf_test = IperfClient.IperfClient('130.56.253.43',5201)
udp_test = UDPClient.UDPClient('130.56.253.43')

# Begin IPERF tests (TCP)

iperf_test.setDownload()
iperf_test.setProtocol('tcp')
iperf_test.run()

iperf_test.setUpload()
iperf_test.run()

results = iperf_test.getResults()

upload_file.json_update_tcp(results)
time.sleep(1)

# 4k test

print 'Starting 4k Video test'

result = udp_test.UDP_Bursty_Download(5206, 1392, 10000, 0.00278, 10)
upload_file.json_update_4k(result)
time.sleep(1)

# 1080p test

print 'Starting 1080p Video test'

result = udp_test.UDP_Bursty_Download(5206, 1392, 10000, 0.011136, 8)
upload_file.json_update_1080p(result)
time.sleep(1)


#720p test

print 'Starting 720p Video test'

result = udp_test.UDP_Bursty_Download(5206, 1392, 10000, 0.0133, 6)
upload_file.json_update_720p(result)
time.sleep(1)

# 480p test


print 'Starting 480p Video test'
result = udp_test.UDP_Bursty_Download(5206, 1392, 10000, 0.0133, 3)
upload_file.json_update_480p(result)
time.sleep(1)


# ScreenSharing 

# Standard def video upload

print 'Starting standard def video upload'
time_profile = [0,3./9,1./9,1./9,2./9,2./9,1./9]
result = udp_test.UDP_Bursty_Upload(5205, 5204, 800, 5000, 0, 5,time_profile)
upload_file.json_update_standard_video_calling(result)
time.sleep(1)

# HD video upload

print 'Starting HD video upload'
result = udp_test.UDP_Bursty_Upload_Uniform(5205,5204,1162,5000, 3, 9, 1, 7)
upload_file.json_update_hd_video_calling(result)
time.sleep(1)


# High Quality VoIP

print 'Starting High Quality VoIP emualtion'
result = udp_test.UDP_Reflector(5209, 160, 500, 50)
upload_file.json_update_high_VOIP(result)
time.sleep(1)

# Low Quality VoIP

print 'Starting Low Quality VoIP emualtion'
result = udp_test.UDP_Reflector(5209, 80, 500, 50)
upload_file.json_update_low_VOIP(result)
time.sleep(1)

# Upload file to server

upload_file.json_upload('130.56.253.43', 5208)


upload_file.print_json()
