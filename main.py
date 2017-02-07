from modules import IperfClient
from lib import jsonprocesser
#from pingClient import pingClient

upload_file = jsonprocesser.jsonprocesser()

iperf_test = IperfClient.IperfClient('130.56.253.43',5201)
#iperf_test.setDownload()
#iperf_test.setProtocol('tcp')

#iperf_test.run()
iperf_results = iperf_test.getResults()
print iperf_results
upload_file.json_update_iperf(iperf_results)
upload_file.json_upload('130.56.253.43',5201)


