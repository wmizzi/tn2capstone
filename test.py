from modules import HTTPClient
import numpy
from modules import UDPClient
from lib import jsonprocesser
from modules import IperfClient
from lib import jsonprocesser
from modules import UDPClient
from threading import Thread
import time

#HTTP_check = HTTPClient.HttpClient()

upload_file = jsonprocesser.jsonprocesser()
iperf_test = IperfClient.IperfClient('130.56.253.43',5201)
udp_test = UDPClient.UDPClient('130.56.253.43')


#print 'Starting 480p Video test'
#result = udp_test.UDP_Bursty_Download(5206, 1000, 4000, 0.04, 7)
#upload_file.json_update_480p(result)
#time.sleep(1)
#print result

upload_file.json_upload('130.56.253.43', 5208)