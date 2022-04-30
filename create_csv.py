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

# command = 'curl -u "707935:MJTXPGwfhnZh5PmK" "https://geolite.info/geoip/v2.1/city/71.192.200.239?pretty"'
# result = json.loads(os.popen(command).read())
# print(result['location'])

import urllib.request
from http.client import *
import sys

ORIGIN = "cs5700cdnorigin.ccs.neu.edu"



def get_content(port, path):
    url = "http://" + ORIGIN + ":" + str(port) + path
    # url = "http://p5-http-b.5700.network:40004/-"
    req = urllib.request.urlopen(url)

    # print(req.getheaders())
    # print(req.getheader("Content-Type"))
    # print(req.getheader("Content-Length"))
    # print(req.getheader("Last-Modified"))
    # print(req.getheader("Accept-Ranges"))
    print(sys.getsizeof(req.read()))


get_content(8080, "/Main_Page")

import socket

# print(socket.gethostbyname("p5-http-a.5700.network"))

REPLICA_INFO = [
    {
        'host': "p5-http-a.5700.network",
        'ip': "50.116.41.109",
        "latitude": 33.844,
        "longitude": -84.4784
    },
    {
        'host': "p5-http-b.5700.network",
        'ip': "45.33.50.187",
        "latitude": 37.5625,
        "longitude": -122.0004
    },
    {
        'host': "p5-http-c.5700.network",
        'ip': "194.195.121.150",
        "latitude": -33.8715,
        "longitude": 151.2006
    },
    {
        'host': "p5-http-d.5700.network",
        'ip': "172.104.144.157",
        "latitude": 50.1188,
        "longitude": 8.6843
    },
    {
        'host': "p5-http-e.5700.network",
        'ip': "172.104.110.211",
        "latitude": 35.6893,
        "longitude": 139.6899
    },
    {
        'host': "p5-http-f.5700.network",
        'ip': "88.80.186.80",
        "latitude": 51.5095,
        "longitude": -0.0955
    },
    {
        'host': "p5-http-g.5700.network",
        'ip': "172.105.55.115",
        "latitude": 19.0748,
        "longitude": 72.8856
    },
]

# for replica in REPLICA_INFO:
#     temp = socket.gethostbyname(replica["host"])
#
#     if temp != replica["ip"]:
#         print(replica)

# file = open("dns-hosts.txt")
# l = []
# # print(file.readlines())
# for line in file.readlines():
#
#     l.append(line.strip())
#
# print(l)
# import csv
# with open('pageviews.csv', newline='') as pages:
#     lines = csv.reader(pages, delimiter=',')
#     i = 0
#     for line in lines:
#         print("/" + line[0])
#         i+= 1
#         if i == 25:
#             break

