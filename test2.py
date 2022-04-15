#!/usr/bin/env python3
import argparse
from dnslib import *
import logging
from mapping import get_nearest_cdn
import sys

BUFFER_SIZE = 4096
TTL = 300
cache = {}


def get_dns_response(data, address, origin_domain):
    origin_domain = origin_domain + "."
    request = DNSRecord.parse(data)
    global cache
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    q_name = str(request.q.qname)
    qtype = request.q.qtype
    qt = QTYPE[request.q.qtype]
    if qt == 'A':
        if q_name == origin_domain or q_name.endswith('.' + origin_domain):
            if address[0] not in cache:
                cache[address[0]] = get_nearest_cdn(address[0])
            ip = cache[address[0]]
            reply.add_answer(RR(rname=qname, rtype=QTYPE.A, ttl=TTL, rdata=A(ip)))

    return reply.pack()


def recv_dns_request(s):
    buffer = b''
    address = None
    while True:
        data, address = s.recvfrom(BUFFER_SIZE)
        buffer += data
        if not data or len(data) < BUFFER_SIZE:
            break
    return buffer, address


def start_dns_server(s, origin_domain):
    while True:
        data, address = recv_dns_request(s)
        response = get_dns_response(data, address, origin_domain)
        s.sendto(response, address)


def main():
    # parser = argparse.ArgumentParser(description='Start a DNS Server.')
    # parser.add_argument(
    #     '-p', type=int, help='Port number that DNS server binds to.', required=True, metavar='port')
    # parser.add_argument(
    #     '-n', type=str, help='CDN-specific name.', required=True, metavar='name')
    # parser.add_argument('--verbose', '-v', help='Print all debug message from dns server', action='store_true')
    #
    # args = parser.parse_args()
    # if args.verbose:
    #     logging.basicConfig(level=logging.DEBUG)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', int(sys.argv[2])))
    try:
        start_dns_server(s, sys.argv[4])
    except KeyboardInterrupt:
        pass
    finally:
        s.close()


if __name__ == '__main__':
    main()