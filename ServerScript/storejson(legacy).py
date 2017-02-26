#Created by Angus Clark 8/01/2017

import json
import os

tempfile = open('temp.json','rb')
info = json.load(tempfile)

id = info["UserInfo"]["user id"]
timestamp = info["UserInfo"]["timestamp"]

os.system('mkdir /home/ubuntu/data/'+id)

path = "/home/ubuntu/data/" + id +"/"
filename = timestamp + '.json'

f = open(path + filename, 'wb')
f.write(tempfile.read())