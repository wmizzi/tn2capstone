from modules import IperfClient
from lib import jsonprocesser
from modules import UDPClient
#from pingClient import pingClient

#udp_test = UDPClient.UDPClient('130.56.253.43')
#udp_test.UDP_Reflector(5203, 1000, 1000, 1000)

upload_file = jsonprocesser.jsonprocesser()

iperf_test = IperfClient.IperfClient('130.56.253.43',5201)

# Download TCP test
iperf_test.setDownload()
iperf_test.setProtocol('tcp')
iperf_test.run()

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
#upload_file.json_upload('130.56.253.43',5202)


