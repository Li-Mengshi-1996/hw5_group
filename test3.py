from dnslib import *


def build_response(data):
    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id,
                                qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    q_type = request.q.qtype
    qt = QTYPE[q_type]

    print(qn)
    return

    # if qt == 'A':
    #     if qn == domain or qn.endswith('.' + domain):
    #         if addr[0] not in cache:
    #             cache[addr[0]] = get_nearest_cdn(addr[0])
    #         ip = cache[addr[0]]
    #         reply.add_answer(RR(rname=qname, rtype=QTYPE.A, rclass=1, ttl=300, rdata=A(ip)))
    #
    # return reply.pack()


# packet = binascii.unhexlify(b'd5ad818000010005000000000377777706676f6f676c6503636f6d0000010001c00c0005000100000005000803777777016cc010c02c0001000100000005000442f95b68c02c0001000100000005000442f95b63c02c0001000100000005000442f95b67c02c0001000100000005000442f95b93')
#
# build_response(packet)

# print('"')
# import sys
#
# test=[1,2,3,4,5,6]
#
# print(sys.getsizeof(test))
# f = open("pageviews.csv")
#
# lines = f.readlines()
#
# for line in lines:
#     print(line)
#     break

# import csv
# with open('pageviews.csv', newline='') as pages:
#     lines = csv.reader(pages, delimiter=',')
#     i = 0
#     for line in lines:
#         print(line)
#
#         i += 1
#
#         if i >= 100:
#             break

from dnslib import *
import sys
import socket
import json
import math
import requests

replica_servers = ["p5-http-a.5700.network", "p5-http-b.5700.network", "p5-http-c.5700.network",
                   "p5-http-d.5700.network", "p5-http-e.5700.network", "p5-http-f.5700.network",
                   "p5-http-g.5700.network"]


def get_geoLocation(ip):
    try:
        url = ('https://geolite.info/geoip/v2.1/city/' + ip + '?pretty')
        response = requests.get(url, auth=('708079', 'xYVsrhhTQiHs9b0M')).content.decode()
        json_str = json.loads(response)
        latitude = json_str['location']['latitude']
        longitude = json_str['location']['longitude']
        return float(latitude), float(longitude)
    except:
        return None, None


def create_replica_info():
    result = []
    for host in replica_servers:
        ip = socket.gethostbyname(host)
        lat, lon = get_geoLocation(ip)
        if lat is None or lon is None:
            lat = 0
            lon = 0

        temp = {"host": host, "ip": ip, "latitude": lat, "longitude": lon}
        result.append(temp)

    return result


# REPLICA_INFO = create_replica_info()
#
# for replica in REPLICA_INFO:
#     print(replica)

# import ipaddress
#
# print(ipaddress.ip_address("50.116.41.109"))
# print(list(ipaddress.ip_network("50.116.32.0/20").hosts()))
import requests
import time

import urllib.request

ORIGIN = "cs5700cdnorigin.ccs.neu.edu"


def get_content(port, path):
    try:
        url = "http://" + ORIGIN + ":" + str(port) + path

        req = requests.get(url).content
        # req = urllib.request.urlopen(url).read()

        return req
    except:
        return b''


t1 = time.time()
print(get_content(8080, '/Doja_Cat')[0:20])
t2 = time.time()
print(t2 - t1)
