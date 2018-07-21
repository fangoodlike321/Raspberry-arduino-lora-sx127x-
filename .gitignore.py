from time import sleep
from urllib import parse,request
import json
import time
import picamera
import requests
url = "http://sunhaojie.applinzi.com/info.php"
req = request.Request(url=url)
res = request.urlopen(req)
res = res.read()
print(res.decode(encoding='utf-8'))
