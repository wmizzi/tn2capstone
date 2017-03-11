import json
import requests

url = 'http://http://stackoverflow.com/questions/4476373/simple-url-get-post-function-in-python'

r = requests.get(url)

r.text