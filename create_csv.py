# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# s.bind(('71.192.200.239',40004))
#
# # print(socket.gethostbyname("cs5700cdn.example.com"))

import os
import json

# command = "scamper -c 'ping -c 1 -i 1' -i 50.116.41.109 -O json"
# print("hello")
# result = os.popen(command).read()
# print(result)

command = 'curl -u "707935:MJTXPGwfhnZh5PmK" "https://geolite.info/geoip/v2.1/city/71.192.200.239?pretty"'
result = json.loads(os.popen(command).read())
# print(result['location'])
