
import time
import pprint
import numpy
length_test = 20
padding = ''
results = []
for j in range(1,20):
    padding = padding + str(1)

for i in range(1,20):
    time.sleep(0.01)
    snt_time = time.time()
    command = str(i) + ',' + str(time.time()) +',' + padding
    print command
    data = command.split(',')
    recv_time = float(time.time()) + 0.3
    latency = recv_time - float(data[1])
    results.append([int(data[0]) , data[1] , recv_time , latency])
    
print results
print type(results)
results.sort(reverse = True)
print results
results.sort()
lat = numpy.asarray(results)
print lat[:][2]

